import React from 'react';
import { useEffect, useState } from 'react';
import styled, { ThemeProvider } from 'styled-components';
import GlobalStyle from './globalStyles';
import { theme } from './theme';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate ,useParams, useLocation } from 'react-router-dom';
import IntroPage from './pages/IntroPage';
import { GameProvider } from './components/GameContext'; // context for exercise

import GamePage from './pages/GamePage'
import { PageProvider } from './components/PageContext'; // context for page
import DataStructureCoursePage from './pages/DataStructureCoursePage';
import TutorialPage from './pages/TutorialPages';
import PythonCoursePage from './pages/PythonCoursePage';
import SystemDesignCoursePage from './pages/SystemDesignCoursePage';
import CoursePage from './pages/CoursePage';
const App: React.FC = () => {
  

  return (
    <div>
      <div>
      <PageProvider>
      <GameProvider>
      <Router>
        {/* <Navigation /> */}
        <Routes>
          <Route path="/" element={<IntroPage />} />
          <Route path="/game/:pageNumber" element={<Page />} />
          <Route path="/datastructurecoursepage" element={<DataStructureCoursePage />} />
          <Route path="/pythoncoursepage" element={<PythonCoursePage />} />
          <Route path="/systemdesigncoursepage" element={<SystemDesignCoursePage />} />
          <Route path="/tutorial" element={<TutorialPage />} />
          <Route path="/coursepage" element={<CoursePage />} />

          {/* <Route path="/Result" element={<Result />} /> */}
        </Routes>
      </Router>
      </GameProvider>
      </PageProvider>

    </div>

    </div>
  );
};

function Navigation() {
  const location = useLocation();
  useEffect(() => {
    // Reset the button state when navigating to the home page
    if (location.pathname === "/") {
      setShowButton(true);
    }
  }, [location]);

  const navigate = useNavigate();
  const [showButton, setShowButton] = useState(true);
  const handleClick = () => {
    setShowButton(false); // Hide button on click
    navigate(`/game/1`);
  };

  return (
    <div>
      {showButton &&(<button onClick={handleClick}>Next </button>)
      }
      {/* <button onClick={() => navigate('/')}>Start Again</button> */}
      </div>
  );
};

interface PageParams {
  pageNumber?: string;
}

function Page() {
  const { pageNumber } = useParams<Record<string, string | undefined>>(); // Use Record to define type
  const page = parseInt(pageNumber || '1', 10); // Convert to an integer, default to 1
  const navigate = useNavigate();

  const handleNext = () => {
    if (page > 9){
      navigate(`/Result`);
    }
    else{
    navigate(`/game/${page + 1}`);}

  };
  const handlePre = () => {
    if (page >= 2){
    navigate(`/game/${page - 1}`);}
  };


  return (
    <div>
      <GamePage page={page} />

      <button onClick={handleNext}>Next</button>
      <button onClick={handlePre}>Previous</button>
      <button onClick={() => navigate('/')}>Start </button>
    </div>
  );
}


export default App;






