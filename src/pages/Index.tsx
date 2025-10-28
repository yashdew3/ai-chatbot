import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { FaRobot, FaCog, FaDatabase, FaComments, FaArrowRight } from 'react-icons/fa';

const Index = () => {
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
                AI Chatbot Management System
              </h1>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                Build, manage, and deploy intelligent chatbots powered by your knowledge base. 
                Upload documents, train your AI, and provide exceptional customer support.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/admin/dashboard">
                <Button className="bg-primary text-primary-foreground hover:bg-primary/90 hover-glow px-8 py-3 text-lg">
                  Admin Dashboard
                  <FaArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Button variant="outline" className="border-border hover:bg-secondary/50 px-8 py-3 text-lg">
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
              Powerful Features for Modern AI
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Everything you need to create and manage intelligent chatbots that understand your business.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="glass-card border-0 hover-lift">
              <CardHeader>
                <div className="p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 w-fit">
                  <FaDatabase className="h-6 w-6 text-blue-400" />
                </div>
                <CardTitle className="text-foreground">Knowledge Base</CardTitle>
                <CardDescription>
                  Upload PDFs, DOCX files, and YouTube videos to train your AI assistant with your specific knowledge.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>• Drag & drop file uploads</li>
                  <li>• YouTube video processing</li>
                  <li>• Real-time indexing status</li>
                  <li>• Content management tools</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="glass-card border-0 hover-lift">
              <CardHeader>
                <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 w-fit">
                  <FaComments className="h-6 w-6 text-green-400" />
                </div>
                <CardTitle className="text-foreground">Smart Chat Widget</CardTitle>
                <CardDescription>
                  Beautiful, responsive chat interface that seamlessly integrates with any website or application.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>• Glassmorphism design</li>
                  <li>• Typing indicators</li>
                  <li>• Mobile responsive</li>
                  <li>• Customizable themes</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="glass-card border-0 hover-lift">
              <CardHeader>
                <div className="p-3 rounded-lg bg-purple-500/10 border border-purple-500/20 w-fit">
                  <FaCog className="h-6 w-6 text-purple-400" />
                </div>
                <CardTitle className="text-foreground">Admin Dashboard</CardTitle>
                <CardDescription>
                  Comprehensive dashboard to monitor performance, manage settings, and analyze user interactions.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>• Real-time analytics</li>
                  <li>• Conversation monitoring</li>
                  <li>• System health status</li>
                  <li>• Customization options</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <Card className="glass-card border-0 text-center p-12">
            <CardHeader>
              <CardTitle className="text-3xl font-bold text-foreground mb-4">
                Ready to Get Started?
              </CardTitle>
              <CardDescription className="text-lg">
                Create your first AI chatbot in minutes. Upload your knowledge base and start providing intelligent customer support.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link to="/login">
                <Button className="bg-primary text-primary-foreground hover:bg-primary/90 hover-glow px-8 py-3 text-lg">
                  Access Admin Panel
                  <FaArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default Index;
