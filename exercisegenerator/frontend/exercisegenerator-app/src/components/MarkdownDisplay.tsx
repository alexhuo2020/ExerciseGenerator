// To display markdown file, support latex math formula using katex package
import 'katex/dist/katex.min.css';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import styled from 'styled-components';

// Define types for options
const options = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
  },
};

// Define prop types
interface MarkdownDisplayProps {
  content: string;
}

// Styled components for ordered lists and list items
const StyledOrderedList = styled.ol`
  padding-left: 20px;
  list-style-type: decimal;
`;

const StyledListItem = styled.li`
  margin-bottom: 4px;
`;

const MarkdownDisplay: React.FC<MarkdownDisplayProps> = ({ content }) => {
  const processedContent = content.replace(/\n/g, '  \n'); // Markdown line breaks (two spaces + newline)

  return (
    <div className="markdown-content">
      <ReactMarkdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[[rehypeKatex, options]]}
        components={{
          ol({ children, ...props }) {
            return <StyledOrderedList {...props}>{children}</StyledOrderedList>;
          },
          li({ children, ...props }) {
            return <StyledListItem {...props}>{children}</StyledListItem>;
          },
          code({ inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
              <SyntaxHighlighter
                style={atomDark}
                language={match[1]}
                PreTag="div"
                showLineNumbers={true}
                {...props}
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            ) : (
              <code className={className} {...props}>
                {children}
              </code>
            );
          },
        }}
      >
        {processedContent}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownDisplay;
