import React, { useState, useEffect } from 'react'; // <--- Add useEffect
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import FileUploader from '../../components/admin/FileUploader';
import KnowledgeBaseTable from '../../components/admin/KnowledgeBaseTable';
import apiClient from '../../services/api'; // <--- IMPORT THE API CLIENT
import { toast } from "@/components/ui/sonner" // <--- Import toast for feedback

export interface KnowledgeItem {
  id: string;
  name: string;
  type: 'pdf' | 'docx' | 'youtube';
  status: 'indexed' | 'processing' | 'error';
  dateAdded: string;
  size?: string;
}

const KnowledgeBase: React.FC = () => {
  // We start with an empty array now, as we will fetch data from the backend
  const [knowledgeItems, setKnowledgeItems] = useState<KnowledgeItem[]>([]);

  // --- START OF MODIFIED CODE ---

  // NOTE: This is a placeholder. A real app would fetch from the backend.
  // We're keeping the mock display for now until you build the GET endpoint.
  useEffect(() => {
    // This is where you would fetch existing knowledge items
    // e.g., apiClient.get('/api/v1/data/sources').then(...)
  }, []);

  const handleUpload = async (files: File[], youtubeUrl?: string) => {
    const formData = new FormData();
    
    // Add all files to the form data
    files.forEach(file => {
      formData.append('files', file);
    });

    // Add the YouTube URL if it exists
    if (youtubeUrl) {
      formData.append('youtube_url', youtubeUrl);
    }
    
    // Check if there is anything to upload
    if (files.length === 0 && !youtubeUrl) {
        toast.warning("No files or URL to upload.");
        return;
    }

    toast.info("Uploading and indexing... This may take a moment.");

    try {
      const response = await apiClient.post('/api/v1/data/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status === 200) {
        toast.success("Knowledge base updated successfully!");
        // Here you would re-fetch the list of knowledge items to update the table
      }
    } catch (error) {
      console.error("Upload failed:", error);
      toast.error("Upload failed. Please check the server logs.");
    }
  };

  const handleDelete = (id: string) => {
    // In a real app, this would be an API call:
    // apiClient.delete(`/api/v1/data/sources/${id}`).then(...)
    setKnowledgeItems(prev => prev.filter(item => item.id !== id));
    toast.success("Source deleted successfully.");
  };

  // --- END OF MODIFIED CODE ---
  
  return (
    <div className="p-6 space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Knowledge Base</h1>
        <p className="text-muted-foreground">
          Upload and manage documents and videos for your AI assistant
        </p>
      </div>

      <Card className="glass-card border-0">
        <CardHeader>
          <CardTitle className="text-foreground">Add Knowledge Sources</CardTitle>
          <CardDescription>
            Upload PDF/DOCX files or add YouTube videos to expand your AI's knowledge
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FileUploader onUpload={handleUpload} />
        </CardContent>
      </Card>

      <Card className="glass-card border-0">
        <CardHeader>
          <CardTitle className="text-foreground">Knowledge Sources</CardTitle>
          <CardDescription>
            Manage your uploaded documents and videos
          </CardDescription>
        </CardHeader>
        <CardContent>
          <KnowledgeBaseTable items={knowledgeItems} onDelete={handleDelete} />
        </CardContent>
      </Card>
    </div>
  );
};

export default KnowledgeBase;