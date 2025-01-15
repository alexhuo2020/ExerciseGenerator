import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Message, PageState } from '../types/types';

interface PageContextType {
  currentPage: number;
  pageStates: Record<number, PageState>;
  setCurrentPage: (page: number) => void;
  updatePageState: (page: number, state: Partial<PageState>) => void;
  getPageState: (page: number) => PageState;
}

const defaultPageState: PageState = {
  messages: [],
  problem: '',
  problemHeight: 400,
  chatHeight: 200,
  inputHeight: 100,
};

const PageContext = createContext<PageContextType | undefined>(undefined);

export const PageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageStates, setPageStates] = useState<Record<number, PageState>>({
    1: { ...defaultPageState },
  });

  const updatePageState = useCallback((page: number, newState: Partial<PageState>) => {
    setPageStates(prev => ({
      ...prev,
      [page]: {
        ...(prev[page] || defaultPageState),
        ...newState,
      },
    }));
  }, []);

  const getPageState = useCallback((page: number) => {
    return pageStates[page] || { ...defaultPageState };
  }, [pageStates]);

  return (
    <PageContext.Provider
      value={{
        currentPage,
        pageStates,
        setCurrentPage,
        updatePageState,
        getPageState,
      }}
    >
      {children}
    </PageContext.Provider>
  );
};

export const usePageContext = () => {
  const context = useContext(PageContext);
  if (!context) {
    throw new Error('usePageContext must be used within a PageProvider');
  }
  return context;
};