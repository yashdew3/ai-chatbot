import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "next-themes";
import ChatDemo from "./pages/ChatDemo";
import NotFound from "./pages/NotFound";
import ChatWidget from "./components/chat/ChatWidget";

const queryClient = new QueryClient();

// Production App - Only ChatDemo and ChatWidget (no admin section)
const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<ChatDemo />} />
            <Route path="/chat" element={<ChatDemo />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
          {/* Chat widget available on all pages */}
          <ChatWidget />
        </BrowserRouter>
      </TooltipProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;