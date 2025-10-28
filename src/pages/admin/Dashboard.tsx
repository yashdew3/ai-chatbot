import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { FaDatabase, FaComments, FaUsers, FaRocket } from 'react-icons/fa';
import ChatWidget from '../../components/chat/ChatWidget';

const Dashboard: React.FC = () => {
  const stats = [
    {
      title: 'Knowledge Sources',
      value: '12',
      description: 'Documents indexed',
      icon: FaDatabase,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
      borderColor: 'border-blue-500/20',
    },
    {
      title: 'Conversations',
      value: '847',
      description: 'This month',
      icon: FaComments,
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
      borderColor: 'border-green-500/20',
    },
    {
      title: 'Active Users',
      value: '156',
      description: 'Last 24 hours',
      icon: FaUsers,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10',
      borderColor: 'border-purple-500/20',
    },
    {
      title: 'Response Time',
      value: '0.8s',
      description: 'Average response',
      icon: FaRocket,
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      borderColor: 'border-primary/20',
    },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
        <p className="text-muted-foreground">
          Monitor your AI chatbot performance and analytics
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <Card
            key={index}
            className={`glass-card border-0 hover-lift ${stat.borderColor}`}
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${stat.bgColor} ${stat.borderColor} border`}>
                <stat.icon className={`h-4 w-4 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground mb-1">
                {stat.value}
              </div>
              <p className="text-xs text-muted-foreground">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="glass-card border-0">
          <CardHeader>
            <CardTitle className="text-foreground">Recent Conversations</CardTitle>
            <CardDescription>
              Latest user interactions with your AI assistant
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { user: 'Anonymous User', message: 'How do I reset my password?', time: '2 minutes ago' },
                { user: 'Anonymous User', message: 'What are your business hours?', time: '15 minutes ago' },
                { user: 'Anonymous User', message: 'Can you help me with pricing?', time: '1 hour ago' },
                { user: 'Anonymous User', message: 'I need technical support', time: '2 hours ago' },
              ].map((conv, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 rounded-lg bg-secondary/30 border border-border/50">
                  <div className="p-2 rounded-full bg-primary/10 border border-primary/20">
                    <FaUsers className="h-3 w-3 text-primary" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground">{conv.user}</p>
                    <p className="text-sm text-muted-foreground truncate">{conv.message}</p>
                    <p className="text-xs text-muted-foreground mt-1">{conv.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card border-0">
          <CardHeader>
            <CardTitle className="text-foreground">System Status</CardTitle>
            <CardDescription>
              Current system health and performance metrics
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { service: 'AI Model', status: 'Operational', color: 'text-green-400', bg: 'bg-green-500/10' },
                { service: 'Knowledge Base', status: 'Operational', color: 'text-green-400', bg: 'bg-green-500/10' },
                { service: 'Chat API', status: 'Operational', color: 'text-green-400', bg: 'bg-green-500/10' },
                { service: 'File Processing', status: 'Processing', color: 'text-yellow-400', bg: 'bg-yellow-500/10' },
              ].map((service, index) => (
                <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-secondary/30 border border-border/50">
                  <span className="text-sm font-medium text-foreground">{service.service}</span>
                  <span className={`text-xs px-2 py-1 rounded-full ${service.bg} ${service.color} border border-current/30`}>
                    {service.status}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Chat Widget for testing */}
      <ChatWidget />
    </div>
  );
};

export default Dashboard;