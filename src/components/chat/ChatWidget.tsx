import React, { useState } from 'react';
import ChatLauncher from './ChatLauncher';
import ChatWindow from './ChatWindow';

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {!isOpen && <ChatLauncher onClick={toggleChat} />}
      {isOpen && <ChatWindow onClose={toggleChat} />}
    </>
  );
};

export default ChatWidget;