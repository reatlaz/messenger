import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css';

import { ConnectedPageChat, ConnectedPageChatList, PageProfile, PageLogin, PageLoginSuccess } from './pages';

function App () {
  // const PrivateRoute = ({ children }) => {
  //   const sessionExpires = JSON.parse(localStorage.getItem('sessionExpires'))
  //   // return children
  //   return (sessionExpires && Date.parse(sessionExpires) > Date.now()) ? children : <Navigate to='/login'/>
  // }
  // const LogInRoute = ({ children }) => {
  //   const sessionExpires = JSON.parse(localStorage.getItem('sessionExpires'))
  //   return (sessionExpires && Date.parse(sessionExpires) > Date.now()) ? <Navigate to='/'/> : children
  // }
  return (
    <Router>
      <div className='App'>
        <Routes>
          <Route path='/login' element={<PageLogin />}/>

          <Route path='/login/success' element={<PageLoginSuccess />}/>

          <Route path='/im' element={<ConnectedPageChatList/>}/>
          <Route path='' element={<ConnectedPageChatList/>}/>
          <Route path='/im/:id' element={<ConnectedPageChat />}/>
          <Route path='/user/:id' element={<PageProfile />}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
