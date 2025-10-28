import React from 'react';
import { FaRobot } from 'react-icons/fa';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex justify-start items-start space-x-2">
      <div className="p-2 rounded-full bg-primary/10 border border-primary/20 mt-1">
        <FaRobot className="h-3 w-3 text-primary" />
      </div>
      
      <div className="bg-secondary/70 text-secondary-foreground p-3 rounded-2xl rounded-bl-sm border border-border/50 animate-fade-in">
        <div className="flex space-x-1">
          <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;