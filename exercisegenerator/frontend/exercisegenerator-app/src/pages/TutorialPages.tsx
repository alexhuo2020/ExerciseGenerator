import React, { useEffect, useState, useRef } from 'react';
import styled from 'styled-components';
import MarkdownDisplay from '../components/MarkdownDisplay';
import { useGameContext } from '../components/GameContext';
import { Link } from 'react-router-dom';
interface TutorialPageProps {
    //   userId: string;
    //   onStartGame: (userId: string, characterName: string, game: string) => void;
    }


const TutorialPage: React.FC<TutorialPageProps> = () => {
    const { gameState } = useGameContext();
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [tutorial, setTutorial] = useState<string>('');

    useEffect(() => {
        const fetchTutorial = async (): Promise<void> => {
          
            setLoading(true);
            console.log(gameState);
            try {
              const response = await fetch('http://localhost:5000/api/tutorial', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(gameState),
              });
              
              if (!response.ok) throw new Error("Failed to fetch data");
              const result = await response.json();
              
              setTutorial(result.tutorial);
            } catch (error) {
              console.error("Error fetching data:", error);
              setError("Failed to load problem.");
            } finally {
              setLoading(false);
            }
        };
    
        fetchTutorial();
      }, [gameState]);
    
    



return (
<TutorialSection>
<Title>{gameState.gameName.toUpperCase() }</Title>
<NavButtons>
        <NavButton to="/game/1">Go to Game</NavButton>
        <NavButton to="/coursepage">Back to Course</NavButton>
      </NavButtons>
<MarkdownDisplay content={tutorial} />
</TutorialSection>
)
};

export default TutorialPage;

interface StyleProps {
    height?: string;
    align?: 'flex-start' | 'flex-end';
    isUser?: boolean;
    inputHeight?: string;
  }
  

  
const BaseSection = styled.div<StyleProps>`
  background-color:#00000;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.3);
`;

const Title = styled.h1`
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 30px;
  font-weight: 600;
  color: #333;
`;

const TutorialSection = styled.div`
  position: relative;
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f7f9fc;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  min-height: 90vh; /* Ensure enough height for layout */
`;

const NavButtons = styled.div`
  position: fixed; /* Ensure buttons are fixed and do not overlap text */
  bottom: 20px; /* Spaced from the bottom of the viewport */
  right: 20px; /* Spaced from the right of the viewport */
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1000; /* Ensure buttons are above other content */
`;

const NavButton = styled(Link)`
  padding: 10px 15px;
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none;
  color: #ffffff;
  background-color: #0077cc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;

  &:hover {
    background-color: #005fa3;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  &:active {
    background-color: #004c82;
  }
`;
