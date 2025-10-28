import React from 'react';
import { Message } from './ChatWindow';
import { FaRobot, FaUser } from 'react-icons/fa';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} items-start space-x-2`}>
      {!isUser && (
        <div className="p-2 rounded-full bg-primary/10 border border-primary/20 mt-1">
          <FaRobot className="h-3 w-3 text-primary" />
        </div>
      )}
      
      <div
        className={`max-w-[80%] p-3 rounded-2xl ${
          isUser
            ? 'bg-primary text-primary-foreground rounded-br-sm'
            : 'bg-secondary/70 text-secondary-foreground rounded-bl-sm border border-border/50'
        } animate-fade-in`}
      >
        <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
        <p className={`text-xs mt-1 ${
          isUser ? 'text-primary-foreground/70' : 'text-muted-foreground'
        }`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>

      {isUser && (
        <div className="p-2 rounded-full bg-secondary/70 border border-border/50 mt-1">
          <FaUser className="h-3 w-3 text-secondary-foreground" />
        </div>
      )}
    </div>
  );
};

export default MessageBubble;