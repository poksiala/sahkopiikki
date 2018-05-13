import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
//import registerServiceWorker from './registerServiceWorker';

if (!process.env.REACT_APP_BACKEND_URL) {
  throw new Error('No backend URL set. Please set REACT_APP_BACKEND_URL in .env!');
}

ReactDOM.render(<App />, document.getElementById('root'));
//registerServiceWorker();
