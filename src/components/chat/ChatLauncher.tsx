import React from 'react';
import { FaComments } from 'react-icons/fa';

interface ChatLauncherProps {
  onClick: () => void;
}

const ChatLauncher: React.FC<ChatLauncherProps> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="fixed bottom-6 right-6 w-14 h-14 bg-primary text-primary-foreground rounded-full shadow-lg hover-glow transition-spring hover:scale-110 animate-float z-50"
      aria-label="Open chat"
    >
      <FaComments className="h-6 w-6 mx-auto" />
    </button>
  );
};

export default ChatLauncher;