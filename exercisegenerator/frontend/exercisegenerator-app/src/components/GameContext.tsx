// GameContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';

interface GameState {
    userName: string,
    characterName: string,
    expertName: string,
    gameName: string,
    problemType: string,
    problemLevel: string
}


interface GameContextType {
  gameState: GameState; 
  setGameState: (info: GameState) => void;

//   setGameState: React.Dispatch<React.SetStateAction<any>>;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

export const GameProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [gameState, setGameState] = useState<GameState>({userName:'', characterName:'', expertName:'', gameName:'', problemType:'', problemLevel:''});

  return (
    <GameContext.Provider value={{ gameState, setGameState }}>
      {children}
    </GameContext.Provider>
  );
};

export const useGameContext = () => {
  const context = useContext(GameContext);
  if (!context) throw new Error("useGameContext must be used within a GameProvider");
  return context;
};
