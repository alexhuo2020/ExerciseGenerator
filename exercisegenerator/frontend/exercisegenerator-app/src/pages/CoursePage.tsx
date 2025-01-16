import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import CourseCard from '../components/CourseCard';

const PageWrapper = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  padding: 20px;
  background-color: #f4f7fc;
`;

const Title = styled.h1`
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 30px;
  font-weight: 600;
  color: #333;
`;

// Styled Link component to remove underline
const StyledLink = styled(Link)`
  text-decoration: none; /* Remove the default underline */
`;



const courses = [
  {
    id: 'pythoncoursepage',
    title: 'Python Programming',
    description: 'Learn the basics of Python programming.',
  },
  {
    id: 'datastructurecoursepage',
    title: 'Data Structure and Algorithms',
    description: 'Master various data structures and algorithms.',
  },
  {
    id: 'systemdesigncoursepage',
    title: 'System Design',
    description: 'Learn the fundamentals of system design and architecture.',
  },
];

const CoursePage: React.FC = () => (
  <div>
    <Title>Start Your Path on Software Engineering</Title>
    <PageWrapper>
      {courses.map((course) => (
        <StyledLink to={`/${course.id}`} key={course.id}>
          <CourseCard title={course.title} description={course.description} />
        </StyledLink>
      ))}
    </PageWrapper>
  </div>
);

export default CoursePage;
