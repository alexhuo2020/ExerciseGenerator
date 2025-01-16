import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import {useGameContext} from '../components/GameContext';

interface IntroPageProps {
//   userId: string;
//   onStartGame: (userId: string, characterName: string, game: string) => void;
}

const IntroPage: React.FC<IntroPageProps> = () => {
  const [userName, setUserName] = useState('');
  const [userId, setUserId] = useState('');
  const [characterName, setCharacterName] = useState('');
  const [expertName, setExpertName] = useState('');
  const [gameName, setGameName] = useState('');
  const [problemType, setProblemType] = useState('');
  const [problemLevel, setProblemLevel] = useState('');
  const navigate = useNavigate();
  const { setGameState } = useGameContext();
  const [selectedProblemTypeIndex, setSelectedProblemTypeIndex] = useState<number | null>(null);
  const ProblemTypeOptions = [ "Multiple Choice", "coding", "T/F", "Eassy",  "Written Response", "Random"];
  const [selectedLevelIndex, setSelectedLevelIndex]  = useState<number | null>(null);
  const LevelOptions = ["Easy", "Intermediate", "Difficult", "Super Difficult", "Random"];

  const [gameId, setGameId] = useState('');


  const onStartGame = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/start_game', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userName,
          userId,
          characterName,
          expertName,
          gameName,
          problemType,
          problemLevel,
        }),
      });

  
      // Check if the response is ok (status in the range 200-299)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      console.log("Response Status:", response.status);
                  
    } catch (error) {
      if (error instanceof Error) {
        console.error('Error saving choice:', error.message);
      } else {
        console.error('An unknown error occurred:', error);
      }
      throw error; // Re-throw the error to be handled by the caller if needed
    }
  };  

  const handleStartGame = async () => {
    if ( userName && userId && characterName && expertName && gameName) {
    onStartGame();
    setGameState({userName, userId, characterName, expertName, gameName, problemType, problemLevel});

      navigate("/game/1") // Move to the first problem

    } else {
      alert('Please enter your name, your ID number and a brief introduction and the task to get started.');
    }
  };

  return (
    <StyledContainer>
      <Title>Welcome </Title>
      <StyledInput
        type="text"
        placeholder="Enter your name."
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />

    <StyledInput
        type="text"
        placeholder="Enter your ID."
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />

      <StyledInput
        type="text"
        placeholder="Enter your role."
        value={characterName}
        onChange={(e) => setCharacterName(e.target.value)}
      />


    <StyledInput
        type="text"
        placeholder="Enter the role of AI expert."
        value={expertName}
        onChange={(e) => setExpertName(e.target.value)}
      />

      <StyledInput
        type="text"
        placeholder="Enter topic you want to challenge yourself."
        value={gameName}
        onChange={(e) => setGameName(e.target.value)}
      />
      
      <OptionsContainer>
        {ProblemTypeOptions.map((option, index) => (
          <Option
            key={index}
            selected={selectedProblemTypeIndex === index}
            onClick={() => {setSelectedProblemTypeIndex(index); setProblemType(ProblemTypeOptions[index])}}
          >
            {option}
          </Option>
        ))}
      </OptionsContainer>

      <OptionsContainer>
        {LevelOptions.map((option, index) => (
          <Option
            key={index}
            selected={selectedLevelIndex === index}
            onClick={() => {setSelectedLevelIndex(index); setProblemLevel(LevelOptions[index])}}
          >
            {option}
          </Option>
        ))}
      </OptionsContainer>


      <StyledButton onClick={handleStartGame}>Get Started</StyledButton>

    </StyledContainer>
  );
};

export default IntroPage;

const StyledContainer = styled.div`
  max-width: 500px;
  margin: 5rem auto;
  padding: 2rem;
  background-color: #2e2e2e; /* Dark background */
  border-radius: 12px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
  text-align: center;
`;

const Title = styled.h1`
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #ffffff; /* Light text color */
`;

const StyledInput = styled.input`
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  background-color: #3c3c3c; /* Dark input background */
  color: #ffffff; /* Light text color */
  border: 1px solid #555555;
  border-radius: 8px;
  box-sizing: border-box;

  ::placeholder {
    color: #aaaaaa; /* Lighter placeholder for readability */
  }
`;

const StyledSelect = styled.select`
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  background-color: #3c3c3c; /* Dark select background */
  color: #ffffff; /* Light text color */
  border: 1px solid #555555;
  border-radius: 8px;
  box-sizing: border-box;
`;

const StyledButton = styled.button`
  width: 100%;
  padding: 0.75rem;
  font-size: 1.1rem;
  font-weight: bold;
  color: #ffffff;
  background-color: #007bff; /* Button color */
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #0056b3; /* Darker button hover */
  }
`;
const OptionsContainer = styled.div`
  width: 100%;
  display: justify;
  flex-direction: row;
  gap: 5px;
  margin-bottom: 1.0rem;
`;

const Option = styled.button<{ selected: boolean }>`
  padding: 10px 20px;
  border: 2px solid ${(props) => (props.selected ? "#4caf50" : "#ccc")};
  border-radius: 8px;
  background-color: ${(props) => (props.selected ? "#e8f5e9" : "#f9f9f9")};
  color: #333;
  cursor: pointer;
  font-size: 8px;
  transition: all 0.3s;

  &:hover {
    border-color: #4caf50;
    background-color: #e8f5e9;
  }
`;

