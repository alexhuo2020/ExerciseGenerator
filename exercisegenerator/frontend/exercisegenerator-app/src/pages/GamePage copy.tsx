import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import MarkdownDisplay from '../components/MarkdownDisplay';
import { useGameContext } from '../components/GameContext';
import { usePageContext } from '../components/PageContext';
import { Message } from '../types/types';



interface GamePageProps {
  page: number;
}

interface StyleProps {
  height?: string;
  align?: 'flex-start' | 'flex-end';
  isUser?: boolean;
  inputHeight?: string;
}

interface APIResponse {
  question: string;
  prediction: string;
}

const GamePage: React.FC<GamePageProps> = ({ page }) => {
    const { gameState } = useGameContext();
    const { updatePageState, getPageState } = usePageContext();
    
    // Local state for input
    const [prompt, setPrompt] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    
    // Get page state
    const pageState = getPageState(page);
    
    // Destructure page state
    const { messages, problem, problemHeight, chatHeight, inputHeight } = pageState;
    
    // Resize state
    const [isDraggingProblem, setIsDraggingProblem] = useState<boolean>(false);
    const [isDraggingChat, setIsDraggingChat] = useState<boolean>(false);
    const [isDraggingInput, setIsDraggingInput] = useState<boolean>(false);
  
    useEffect(() => {
      const fetchProblem = async (): Promise<void> => {
        // Only fetch if we don't have the problem already
        if (!pageState.problem) {
          setLoading(true);
          try {
            const response = await fetch('http://localhost:5000/api/problem', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(gameState),
            });
            
            if (!response.ok) throw new Error("Failed to fetch data");
            const result = await response.json();
            
            updatePageState(page, { problem: result.question });
          } catch (error) {
            console.error("Error fetching data:", error);
            setError("Failed to load problem.");
          } finally {
            setLoading(false);
          }
        }
      };
  
      fetchProblem();
    }, [page, gameState, pageState.problem, updatePageState]);
  
    const sendMessage = async (): Promise<void> => {
      if (!prompt) return;
  
      const newMessages = [...messages, { author: 'user', content: prompt } as Message];
      updatePageState(page, { messages: newMessages });
  
      try {
        const response = await fetch('http://localhost:5000/api/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ problem, prompt, history: messages }),
        });
        
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        
        updatePageState(page, {
          messages: [...newMessages, { author: 'AI', content: data.prediction } as Message],
        });
      } catch (error) {
        console.error('Error sending message:', error);
      }
      
      setPrompt('');
    };
  
    // Handle mouse movement for resizing
    useEffect(() => {
      const handleMouseMove = (e: MouseEvent): void => {
        if (isDraggingProblem) {
          const newHeight = e.clientY;
          const newProblemHeight = Math.max(100, Math.min(newHeight, window.innerHeight - 400));
          updatePageState(page, { problemHeight: newProblemHeight });
        } else if (isDraggingChat) {
          const newHeight = window.innerHeight - e.clientY - inputHeight - 50;
          const newChatHeight = Math.max(100, Math.min(newHeight, window.innerHeight - problemHeight - inputHeight - 100));
          updatePageState(page, { chatHeight: newChatHeight });
        } else if (isDraggingInput) {
          const totalAvailableHeight = window.innerHeight - problemHeight - 50;
          const newInputHeight = Math.max(80, Math.min(300, window.innerHeight - e.clientY));
          const newChatHeight = totalAvailableHeight - newInputHeight;
          
          if (newChatHeight >= 100) {
            updatePageState(page, {
              inputHeight: newInputHeight,
              chatHeight: newChatHeight,
            });
          }
        }
      };
  
      const handleMouseUp = (): void => {
        setIsDraggingProblem(false);
        setIsDraggingChat(false);
        setIsDraggingInput(false);
      };
  
      if (isDraggingProblem || isDraggingChat || isDraggingInput) {
        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('mouseup', handleMouseUp);
      }
  
      return () => {
        window.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('mouseup', handleMouseUp);
      };
    }, [isDraggingProblem, isDraggingChat, isDraggingInput, page, problemHeight, inputHeight, updatePageState]);
  
    if (loading) return <div>Loading...</div>;
  
    return (
      <ChatbotContainer>
        <ProblemSection height={`${problemHeight}px`}>
          <MarkdownDisplay content={problem} />
        </ProblemSection>
        
        <ResizeHandle
          onMouseDown={() => setIsDraggingProblem(true)}
          className={isDraggingProblem ? 'active' : ''}
        />
        
        <MessageSection height={`${chatHeight}px`}>
          {messages.map((message, index) => (
            <MessageContainer
              key={index}
              align={message.author === 'user' ? 'flex-end' : 'flex-start'}
            >
              <MessageBubble isUser={message.author === 'user'}>
                <MarkdownDisplay content={message.content} />
              </MessageBubble>
            </MessageContainer>
          ))}
        </MessageSection>
        
        <ResizeHandle
          onMouseDown={() => setIsDraggingChat(true)}
          className={isDraggingChat ? 'active' : ''}
        />
  
        <InputSection inputHeight={`${inputHeight}px`}>
          <TextArea
            value={prompt}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setPrompt(e.target.value)}
            placeholder="Type your message..."
            style={{ height: `${inputHeight - 20}px` }}
          />
          <SendButton onClick={sendMessage}>Send</SendButton>
        </InputSection>

        <ResizeHandle
          onMouseDown={() => setIsDraggingInput(true)}
          className={isDraggingInput? 'active' : ''}
        />

      </ChatbotContainer>
    );
  };
  
  export default GamePage;
  
// Styled Components
const ChatbotContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: 'Inter', sans-serif;
  background-color: #121212;
  color: #e0e0e0;
  overflow: hidden;
`;

const ResizeHandle = styled.div`
  height: 8px;
  background-color: #2a2a2a;
  cursor: row-resize;
  transition: background-color 0.2s;
  
  &:hover, &.active {
    background-color: #4caf50;
  }
  
  &::after {
    content: '';
    display: block;
    height: 2px;
    margin: 3px auto;
    width: 40px;
    background-color: #444;
  }
`;

const BaseSection = styled.div<StyleProps>`
  padding: 20px;
  background-color: #1e1e1e;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.3);
  overflow-y: auto;
`;

const ProblemSection = styled(BaseSection)`
  height: ${props => props.height};
  flex-shrink: 0;
  font-size: 16px;
  line-height: 1.6;
  background-color: #252525;
`;

const MessageSection = styled(BaseSection)`
//   height: ${props => props.height};
  flex-shrink: 0;
`;

const MessageContainer = styled.div<StyleProps>`
  display: flex;
  justify-content: ${props => props.align};
  margin-bottom: 10px;
`;

const MessageBubble = styled.div<StyleProps>`
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 15px;
  background-color: ${props => props.isUser ? '#4caf50' : '#333'};
  color: ${props => props.isUser ? '#fff' : '#e0e0e0'};
  font-size: 14px;
  line-height: 1.5;
  margin: 5px 0;
  word-wrap: break-word;
  white-space: pre-wrap;
`;

const InputSection = styled.div<StyleProps>`
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #1c1c1c;
  border-top: 1px solid #444;
height: ${props => props.inputHeight || '100px'};
`;

const TextArea = styled.textarea`
  flex: 1;
  padding: 10px 15px;
  border-radius: 12px;
  border: none;
  outline: none;
  font-size: 14px;
  resize: none;
  background-color: #2a2a2a;
  color: #e0e0e0;
  overflow-y: auto;
`;

const SendButton = styled.button`
  padding: 10px 20px;
  margin-left: 10px;
  border-radius: 20px;
  background-color: #4caf50;
  color: #ffffff;
  border: none;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.3s ease;

  &:hover {
    background-color: #45a049;
    transform: scale(1.05);
  }

  &:active {
    transform: scale(0.95);
  }
`;