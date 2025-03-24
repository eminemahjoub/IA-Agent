import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import AuthContext from '../../context/auth/authContext';

const PrivateRoute = ({ component: Component }) => {
  const authContext = useContext(AuthContext);
  const { isAuthenticated, loading } = authContext;

  if (loading) {
    return <div>Loading...</div>;
  }

  if (isAuthenticated) {
    return <Component />;
  } else {
    return <Navigate to="/login" />;
  }
};

export default PrivateRoute; 