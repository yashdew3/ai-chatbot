import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Switch } from '../../components/ui/switch';
import { toast } from '../../hooks/use-toast';
import { FaRobot, FaPalette, FaCog, FaBell } from 'react-icons/fa';

const Settings: React.FC = () => {
  const [settings, setSettings] = useState({
    botName: 'AI Assistant',
    welcomeMessage: 'Hello! How can I help you today?',
    responseDelay: '1000',
    enableTypingIndicator: true,
    enableNotifications: true,
    maxMessageLength: '1000',
    primaryColor: '#00FFFF',
    enableAnalytics: true,
  });

  const handleSave = async () => {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    toast({
      title: "Settings saved",
      description: "Your chatbot settings have been updated successfully.",
    });
  };

  const handleInputChange = (key: string, value: string | boolean) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="p-6 space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground">
          Configure your AI chatbot behavior and appearance
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bot Configuration */}
        <Card className="glass-card border-0">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <FaRobot className="h-5 w-5 text-primary" />
              <CardTitle className="text-foreground">Bot Configuration</CardTitle>
            </div>
            <CardDescription>
              Customize your chatbot's basic settings
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="botName">Bot Name</Label>
              <Input
                id="botName"
                value={settings.botName}
                onChange={(e) => handleInputChange('botName', e.target.value)}
                className="bg-input border-border"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="welcomeMessage">Welcome Message</Label>
              <Textarea
                id="welcomeMessage"
                value={settings.welcomeMessage}
                onChange={(e) => handleInputChange('welcomeMessage', e.target.value)}
                className="bg-input border-border min-h-[80px]"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="responseDelay">Response Delay (ms)</Label>
              <Input
                id="responseDelay"
                type="number"
                value={settings.responseDelay}
                onChange={(e) => handleInputChange('responseDelay', e.target.value)}
                className="bg-input border-border"
              />
            </div>
          </CardContent>
        </Card>

        {/* Appearance */}
        <Card className="glass-card border-0">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <FaPalette className="h-5 w-5 text-primary" />
              <CardTitle className="text-foreground">Appearance</CardTitle>
            </div>
            <CardDescription>
              Customize the visual appearance of your chatbot
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="primaryColor">Primary Color</Label>
              <div className="flex items-center space-x-2">
                <Input
                  id="primaryColor"
                  type="color"
                  value={settings.primaryColor}
                  onChange={(e) => handleInputChange('primaryColor', e.target.value)}
                  className="w-12 h-10 p-1 border-border"
                />
                <Input
                  value={settings.primaryColor}
                  onChange={(e) => handleInputChange('primaryColor', e.target.value)}
                  className="bg-input border-border"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="maxMessageLength">Max Message Length</Label>
              <Input
                id="maxMessageLength"
                type="number"
                value={settings.maxMessageLength}
                onChange={(e) => handleInputChange('maxMessageLength', e.target.value)}
                className="bg-input border-border"
              />
            </div>
          </CardContent>
        </Card>

        {/* Features */}
        <Card className="glass-card border-0">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <FaCog className="h-5 w-5 text-primary" />
              <CardTitle className="text-foreground">Features</CardTitle>
            </div>
            <CardDescription>
              Enable or disable chatbot features
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Typing Indicator</Label>
                <p className="text-sm text-muted-foreground">Show typing dots when bot is responding</p>
              </div>
              <Switch
                checked={settings.enableTypingIndicator}
                onCheckedChange={(checked) => handleInputChange('enableTypingIndicator', checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Analytics</Label>
                <p className="text-sm text-muted-foreground">Track conversation metrics</p>
              </div>
              <Switch
                checked={settings.enableAnalytics}
                onCheckedChange={(checked) => handleInputChange('enableAnalytics', checked)}
              />
            </div>
          </CardContent>
        </Card>

        {/* Notifications */}
        <Card className="glass-card border-0">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <FaBell className="h-5 w-5 text-primary" />
              <CardTitle className="text-foreground">Notifications</CardTitle>
            </div>
            <CardDescription>
              Configure notification preferences
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Enable Notifications</Label>
                <p className="text-sm text-muted-foreground">Receive alerts for new conversations</p>
              </div>
              <Switch
                checked={settings.enableNotifications}
                onCheckedChange={(checked) => handleInputChange('enableNotifications', checked)}
              />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button 
          onClick={handleSave}
          className="bg-primary text-primary-foreground hover:bg-primary/90 hover-glow"
        >
          Save Settings
        </Button>
      </div>
    </div>
  );
};

export default Settings;