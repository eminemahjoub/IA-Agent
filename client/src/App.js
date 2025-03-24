import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

// Components
import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';
import Dashboard from './components/dashboard/Dashboard';
import Landing from './components/layout/Landing';
import Register from './components/auth/Register';
import Login from './components/auth/Login';
import Alert from './components/layout/Alert';
import PrivateRoute from './components/routing/PrivateRoute';
import TaskDashboard from './components/tasks/TaskDashboard';
import HabitDashboard from './components/habits/HabitDashboard';
import FocusMode from './components/focus/FocusMode';
import EmailDashboard from './components/email/EmailDashboard';
import CalendarDashboard from './components/calendar/CalendarDashboard';
import Settings from './components/settings/Settings';
import VoiceAssistant from './components/assistant/VoiceAssistant';

// Context
import AuthState from './context/auth/AuthState';
import AlertState from './context/alert/AlertState';
import TaskState from './context/task/TaskState';
import HabitState from './context/habit/HabitState';
import FocusState from './context/focus/FocusState';

// Theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#3f51b5',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 500,
    },
    h2: {
      fontWeight: 500,
    },
    h3: {
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
        },
      },
    },
  },
});

const App = () => {
  const [drawerOpen, setDrawerOpen] = useState(true);

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 960) {
        setDrawerOpen(false);
      } else {
        setDrawerOpen(true);
      }
    };

    // Initial check
    handleResize();

    // Add event listener
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <AuthState>
      <TaskState>
        <HabitState>
          <FocusState>
            <AlertState>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <ThemeProvider theme={theme}>
                  <CssBaseline />
                  <Router>
                    <Box sx={{ display: 'flex' }}>
                      <Navbar toggleDrawer={toggleDrawer} />
                      <Sidebar open={drawerOpen} toggleDrawer={toggleDrawer} />
                      <Box
                        component="main"
                        sx={{
                          flexGrow: 1,
                          p: 3,
                          width: { sm: `calc(100% - ${drawerOpen ? 240 : 0}px)` },
                          ml: { sm: `${drawerOpen ? 240 : 0}px` },
                          mt: '64px',
                          transition: 'margin 0.2s ease',
                          minHeight: 'calc(100vh - 64px)',
                        }}
                      >
                        <Alert />
                        <Routes>
                          <Route path="/" element={<Landing />} />
                          <Route path="/register" element={<Register />} />
                          <Route path="/login" element={<Login />} />
                          <Route
                            path="/dashboard"
                            element={<PrivateRoute component={Dashboard} />}
                          />
                          <Route
                            path="/tasks"
                            element={<PrivateRoute component={TaskDashboard} />}
                          />
                          <Route
                            path="/habits"
                            element={<PrivateRoute component={HabitDashboard} />}
                          />
                          <Route
                            path="/focus"
                            element={<PrivateRoute component={FocusMode} />}
                          />
                          <Route
                            path="/email"
                            element={<PrivateRoute component={EmailDashboard} />}
                          />
                          <Route
                            path="/calendar"
                            element={<PrivateRoute component={CalendarDashboard} />}
                          />
                          <Route
                            path="/settings"
                            element={<PrivateRoute component={Settings} />}
                          />
                        </Routes>
                      </Box>
                      <VoiceAssistant />
                    </Box>
                  </Router>
                </ThemeProvider>
              </LocalizationProvider>
            </AlertState>
          </FocusState>
        </HabitState>
      </TaskState>
    </AuthState>
  );
};

export default App; 