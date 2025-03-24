import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Box, TextField, Button, Typography, Paper, List, ListItem, ListItemText, Divider, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import MicIcon from '@mui/icons-material/Mic';

const CommandInput = () => {
  const [command, setCommand] = useState('');
  const [processing, setProcessing] = useState(false);
  const [conversation, setConversation] = useState([]);
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);
  const conversationEndRef = useRef(null);

  // Initialize speech recognition if available
  useEffect(() => {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setCommand(transcript);
        setListening(false);
      };
      
      recognitionRef.current.onend = () => {
        setListening(false);
      };
    }
  }, []);

  // Scroll to bottom of conversation when it updates
  useEffect(() => {
    if (conversationEndRef.current) {
      conversationEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [conversation]);

  const handleCommandChange = (e) => {
    setCommand(e.target.value);
  };

  const toggleListening = () => {
    if (!recognitionRef.current) return;
    
    if (!listening) {
      recognitionRef.current.start();
      setListening(true);
    } else {
      recognitionRef.current.stop();
      setListening(false);
    }
  };

  const sendCommand = async () => {
    if (!command.trim()) return;
    
    // Add user message to conversation
    setConversation(prev => [...prev, { type: 'user', text: command }]);
    
    setProcessing(true);
    try {
      const res = await axios.post('/api/commands', { text: command });
      
      // Add assistant response to conversation
      setConversation(prev => [...prev, { 
        type: 'assistant', 
        text: res.data.response.message,
        data: res.data.response.data 
      }]);
      
      // Clear command input
      setCommand('');
    } catch (err) {
      setConversation(prev => [...prev, { 
        type: 'error', 
        text: 'Sorry, I encountered an error processing your request.' 
      }]);
      console.error('Error sending command:', err);
    } finally {
      setProcessing(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendCommand();
    }
  };

  const renderConversationItem = (item, index) => {
    if (item.type === 'user') {
      return (
        <ListItem key={index} sx={{ justifyContent: 'flex-end' }}>
          <Paper elevation={1} sx={{ 
            p: 2, 
            bgcolor: 'primary.light', 
            color: 'primary.contrastText',
            maxWidth: '80%',
            borderRadius: '20px 20px 5px 20px'
          }}>
            <Typography>{item.text}</Typography>
          </Paper>
        </ListItem>
      );
    } else if (item.type === 'assistant') {
      return (
        <ListItem key={index} sx={{ justifyContent: 'flex-start' }}>
          <Paper elevation={1} sx={{ 
            p: 2, 
            bgcolor: 'grey.100',
            maxWidth: '80%',
            borderRadius: '20px 20px 20px 5px'
          }}>
            <Typography>{item.text}</Typography>
            {item.data && item.data.length > 0 && (
              <Box mt={1}>
                {item.data.map((dataItem, i) => (
                  <Box key={i} p={1} mb={1} bgcolor="rgba(0,0,0,0.03)" borderRadius={1}>
                    <Typography variant="body2">{dataItem.title || dataItem.name}</Typography>
                    {dataItem.description && (
                      <Typography variant="caption" display="block">{dataItem.description}</Typography>
                    )}
                  </Box>
                ))}
              </Box>
            )}
          </Paper>
        </ListItem>
      );
    } else {
      // Error message
      return (
        <ListItem key={index} sx={{ justifyContent: 'center' }}>
          <Paper elevation={1} sx={{ 
            p: 2, 
            bgcolor: 'error.light',
            color: 'error.contrastText',
            maxWidth: '80%',
            borderRadius: '20px'
          }}>
            <Typography>{item.text}</Typography>
          </Paper>
        </ListItem>
      );
    }
  };

  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      height: '100%', 
      maxHeight: '600px',
      borderRadius: 2,
      overflow: 'hidden',
      boxShadow: 3
    }}>
      {/* Conversation history */}
      <Box sx={{ 
        flex: 1, 
        overflowY: 'auto', 
        p: 2,
        bgcolor: 'background.default'
      }}>
        <List>
          {conversation.length === 0 ? (
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center', 
              height: '100%',
              opacity: 0.6 
            }}>
              <Typography variant="body1" color="textSecondary">
                Try asking me to "create a task" or "list my habits"
              </Typography>
            </Box>
          ) : (
            conversation.map(renderConversationItem)
          )}
          <div ref={conversationEndRef} />
        </List>
      </Box>
      
      <Divider />
      
      {/* Command input */}
      <Box sx={{ p: 2, bgcolor: 'background.paper' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type a command..."
            value={command}
            onChange={handleCommandChange}
            onKeyPress={handleKeyPress}
            disabled={processing}
            sx={{ mr: 1 }}
          />
          
          <Button
            variant="contained"
            color="primary"
            onClick={toggleListening}
            disabled={processing || !recognitionRef.current}
            sx={{ minWidth: '50px', mr: 1 }}
          >
            <MicIcon sx={{ color: listening ? 'error.main' : 'inherit' }} />
          </Button>
          
          <Button
            variant="contained"
            color="primary"
            onClick={sendCommand}
            disabled={!command.trim() || processing}
            endIcon={processing ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
          >
            Send
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default CommandInput; 