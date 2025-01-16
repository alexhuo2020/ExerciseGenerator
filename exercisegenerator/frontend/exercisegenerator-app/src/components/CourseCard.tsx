import React from 'react';
import styled from 'styled-components';

interface CourseCardProps {
  title: string;
  description: string;
}

const CardWrapper = styled.div`
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  width: 280px;
  height: 150px; /* Fixed height */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }
`;

const CardContent = styled.div`
  padding: 20px;
  overflow: hidden; /* Ensures text does not overflow */
`;

const Title = styled.h3`
  margin: 0;
  font-size: 1.5rem;
  color: #333;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis; /* Truncate text if too long */
  white-space: nowrap; /* Prevent text from wrapping */
`;

const Description = styled.p`
  margin-top: 10px;
  font-size: 1rem;
  color: #555;
  flex-grow: 1; /* Allow description to take available space */
  overflow: hidden;
  text-overflow: ellipsis; /* Truncate long descriptions */
`;

const CourseCard: React.FC<CourseCardProps> = ({ title, description }) => (
  <CardWrapper>
    <CardContent>
      <Title>{title}</Title>
      <Description>{description}</Description>
    </CardContent>
  </CardWrapper>
);

export default CourseCard;
