export interface Message {
    author: 'user' | 'AI';
    content: string;
  }
  
  export interface PageState {
    messages: Message[];
    problem: string;
    problemHeight: number;
    chatHeight: number;
    inputHeight: number;
  }
  