import React from 'react';
import ReactDOM from 'react-dom';
import Dashboard from './components/Dashboard';
import { BrowserRouter as Router } from 'react-router';
import $ from 'jquery';

if (process.env.NODE_ENV !== 'production') {
    window.$ = $;
}

const app = document.getElementById('root');

ReactDOM.render(
    <Router basename="/">
        <Dashboard />
    </Router>, app
);