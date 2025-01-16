import React, { useState } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { useGameContext } from "../components/GameContext";
import courseData from "../contents/pythoncourse.json";

const Title = styled.h1`
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 30px;
  font-weight: 600;
  color: #333;
`;
 
const CourseContainer = styled.div`
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f7f9fc;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const SectionTitle = styled.h2`
  font-size: 1.8rem;
  margin-top: 30px;
  margin-bottom: 15px;
  color: #222;
  font-weight: 600;
  border-bottom: 2px solid #ccc;
  padding-bottom: 5px;
`;

const TopicLink = styled(Link)`
  display: block;
  padding: 10px 15px;
  margin: 5px 0;
  text-decoration: none;
  color: #444;
  font-size: 1.2rem;
  font-weight: 500;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;

  &:hover {
    background-color: #e6f7ff;
    color: #0077cc;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  }

  &:active {
    background-color: #cce6ff;
  }
`;

interface Course {
  course: string;
  sections: Section[];
}

interface Section {
  title: string;
  topics: string[];
}

const PythonCoursePage = () => {
  const { gameState, setGameState } = useGameContext();
  const userName = "Alex";
  const userId = "00001";
  const characterName = "software engineer";
  const expertName = "software engineer";
  const [gameName, setGameName] = useState<string>("");
  const problemType = "coding";
  const problemLevel = "Random";

  const updateAllState = (topic: string) => {
    setGameState({
      userName: userName,
      userId: userId,
      characterName: characterName,
      expertName: expertName,
      gameName: topic,
      problemType: problemType,
      problemLevel: problemLevel,
    });
  };

  const course: Course = courseData;

  return (
    <CourseContainer>
      <Title>Welcome to the Course: Python Programming</Title>
      <p style={{ textAlign: "center", fontSize: "1.1rem", color: "#666" }}>
        Select a topic to start learning
      </p>

      {course.sections.map((section, sectionIndex) => (
        <div key={sectionIndex}>
          <SectionTitle>{section.title}</SectionTitle>
          {section.topics.map((topic, topicIndex) => (
            <TopicLink
              key={topicIndex}
              to={`/tutorial`}
              onClick={() => updateAllState(topic)}
            >
              {topic}
            </TopicLink>
          ))}
        </div>
      ))}
    </CourseContainer>
  );
};

export default PythonCoursePage;
