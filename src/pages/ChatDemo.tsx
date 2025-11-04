import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { FaRobot, FaComments, FaLightbulb, FaRocket } from 'react-icons/fa';
import ChatWindow from '../components/chat/ChatWindow';

const ChatDemo = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleTryChat = () => {
    setIsChatOpen(true);
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="container mx-auto px-4 py-20">
          <div className="text-center space-y-8">
            <div className="flex justify-center">
              <div className="p-6 rounded-full bg-primary/10 border border-primary/20 animate-glow">
                <FaRobot className="h-12 w-12 text-primary" />
              </div>
            </div>
            
            <div className="space-y-4">
              <h1 className="text-5xl font-bold bg-gradient-primary bg-clip-text text-transparent">
                AI-Powered Chat Assistant
              </h1>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                Experience our intelligent chatbot powered by advanced AI. Ask questions and get instant, 
                accurate answers from our comprehensive knowledge base.
              </p>
            </div>

            <div className="flex justify-center">
              <Button 
                onClick={handleTryChat}
                className="bg-primary text-primary-foreground hover:bg-primary/90 hover-glow px-8 py-3 text-lg"
              >
                Try Demo Chat
                <FaComments className="ml-2 h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-foreground mb-4">
              Why Choose Our AI Assistant?
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Built with cutting-edge technology to provide you with the best conversational experience.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="glass-card border-0 hover-lift">
              <CardHeader>
                <div className="p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 w-fit">
                  <FaLightbulb className="h-6 w-6 text-blue-400" />
                </div>
                <CardTitle className="text-foreground">Intelligent Responses</CardTitle>
                <CardDescription>
                  Our AI understands context and provides relevant, accurate answers to your questions.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>• Natural language processing</li>
                  <li>• Context-aware responses</li>
                  <li>• Continuous learning</li>
                  <li>• Multi-topic support</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="glass-card border-0 hover-lift">
              <CardHeader>
                <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 w-fit">
                  <FaRocket className="h-6 w-6 text-green-400" />
                </div>
                <CardTitle className="text-foreground">Lightning Fast</CardTitle>
                <CardDescription>
                  Get instant responses powered by advanced AI technology and optimized performance.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>• Sub-second response time</li>
                  <li>• Real-time processing</li>
                  <li>• Scalable architecture</li>
                  <li>• 24/7 availability</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="glass-card border-0 hover-lift">
              <CardHeader>
                <div className="p-3 rounded-lg bg-purple-500/10 border border-purple-500/20 w-fit">
                  <FaComments className="h-6 w-6 text-purple-400" />
                </div>
                <CardTitle className="text-foreground">Seamless Integration</CardTitle>
                <CardDescription>
                  Beautiful, responsive chat interface that works perfectly on any device or platform.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>• Mobile-first design</li>
                  <li>• Cross-platform compatibility</li>
                  <li>• Easy integration</li>
                  <li>• Customizable appearance</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Demo Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <Card className="glass-card border-0 text-center p-12">
            <CardHeader>
              <CardTitle className="text-3xl font-bold text-foreground mb-4">
                Ready to Experience AI Chat?
              </CardTitle>
              <CardDescription className="text-lg">
                Start a conversation with our AI assistant. Ask any question and see the magic happen!
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                  <div className="text-left p-4 rounded-lg bg-secondary/20 border border-secondary/30">
                    <h4 className="font-semibold text-sm text-foreground mb-2">Try asking:</h4>
                    <p className="text-xs text-muted-foreground">"What services do you offer?"</p>
                  </div>
                  <div className="text-left p-4 rounded-lg bg-secondary/20 border border-secondary/30">
                    <h4 className="font-semibold text-sm text-foreground mb-2">Or ask about:</h4>
                    <p className="text-xs text-muted-foreground">"How can I get help?"</p>
                  </div>
                </div>
                <Button 
                  onClick={handleTryChat}
                  className="bg-primary text-primary-foreground hover:bg-primary/90 hover-glow px-8 py-3 text-lg"
                >
                  Start Chatting Now
                  <FaComments className="ml-2 h-5 w-5" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Chat Widget */}
      {isChatOpen && (
        <ChatWindow onClose={() => setIsChatOpen(false)} />
      )}
    </div>
  );
};

export default ChatDemo;