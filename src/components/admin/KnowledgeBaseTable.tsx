import React, { useState } from 'react';
import { Button } from '../ui/button';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '../ui/table';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '../ui/alert-dialog';
import { FaFilePdf, FaFileWord, FaYoutube, FaTrash, FaCheckCircle, FaSpinner, FaExclamationCircle } from 'react-icons/fa';
import { KnowledgeItem } from '../../pages/admin/KnowledgeBase';

interface KnowledgeBaseTableProps {
  items: KnowledgeItem[];
  onDelete: (id: string) => void;
}

const KnowledgeBaseTable: React.FC<KnowledgeBaseTableProps> = ({ items, onDelete }) => {
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const handleDelete = async (id: string) => {
    setDeletingId(id);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500));
    onDelete(id);
    setDeletingId(null);
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'pdf':
        return <FaFilePdf className="h-4 w-4 text-red-400" />;
      case 'docx':
        return <FaFileWord className="h-4 w-4 text-blue-400" />;
      case 'youtube':
        return <FaYoutube className="h-4 w-4 text-red-500" />;
      default:
        return <FaFilePdf className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'indexed':
        return (
          <div className="status-indexed px-3 py-1 rounded-full text-xs font-medium flex items-center space-x-1">
            <FaCheckCircle className="h-3 w-3" />
            <span>Indexed</span>
          </div>
        );
      case 'processing':
        return (
          <div className="status-processing px-3 py-1 rounded-full text-xs font-medium flex items-center space-x-1">
            <FaSpinner className="h-3 w-3 animate-spin" />
            <span>Processing</span>
          </div>
        );
      case 'error':
        return (
          <div className="status-error px-3 py-1 rounded-full text-xs font-medium flex items-center space-x-1">
            <FaExclamationCircle className="h-3 w-3" />
            <span>Error</span>
          </div>
        );
      default:
        return null;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="space-y-4">
      {items.length === 0 ? (
        <div className="text-center py-12">
          <div className="flex justify-center mb-4">
            <div className="p-4 rounded-full bg-muted">
              <FaFilePdf className="h-8 w-8 text-muted-foreground" />
            </div>
          </div>
          <h3 className="text-lg font-medium text-foreground mb-2">No knowledge sources</h3>
          <p className="text-muted-foreground">
            Upload your first document or add a YouTube video to get started.
          </p>
        </div>
      ) : (
        <div className="rounded-lg border border-border overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="bg-secondary/30 hover:bg-secondary/50">
                <TableHead className="text-foreground font-medium">Source</TableHead>
                <TableHead className="text-foreground font-medium">Type</TableHead>
                <TableHead className="text-foreground font-medium">Date Added</TableHead>
                <TableHead className="text-foreground font-medium">Status</TableHead>
                <TableHead className="text-foreground font-medium">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.map((item) => (
                <TableRow key={item.id} className="hover:bg-secondary/20">
                  <TableCell>
                    <div className="flex items-center space-x-3">
                      {getTypeIcon(item.type)}
                      <div>
                        <p className="font-medium text-foreground">{item.name}</p>
                        {item.size && (
                          <p className="text-sm text-muted-foreground">{item.size}</p>
                        )}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm text-muted-foreground uppercase">
                      {item.type}
                    </span>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm text-muted-foreground">
                      {formatDate(item.dateAdded)}
                    </span>
                  </TableCell>
                  <TableCell>
                    {getStatusBadge(item.status)}
                  </TableCell>
                  <TableCell>
                    <AlertDialog>
                      <AlertDialogTrigger asChild>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-8 w-8 p-0 hover:bg-destructive/10 hover:text-destructive"
                          disabled={deletingId === item.id}
                        >
                          {deletingId === item.id ? (
                            <FaSpinner className="h-3 w-3 animate-spin" />
                          ) : (
                            <FaTrash className="h-3 w-3" />
                          )}
                        </Button>
                      </AlertDialogTrigger>
                      <AlertDialogContent className="glass-card border-0">
                        <AlertDialogHeader>
                          <AlertDialogTitle className="text-foreground">
                            Delete Knowledge Source
                          </AlertDialogTitle>
                          <AlertDialogDescription className="text-muted-foreground">
                            Are you sure you want to delete "{item.name}"? This action cannot be undone and will remove all associated knowledge from your AI assistant.
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel className="bg-secondary text-secondary-foreground hover:bg-secondary/80">
                            Cancel
                          </AlertDialogCancel>
                          <AlertDialogAction
                            onClick={() => handleDelete(item.id)}
                            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                          >
                            Delete
                          </AlertDialogAction>
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
};

export default KnowledgeBaseTable;