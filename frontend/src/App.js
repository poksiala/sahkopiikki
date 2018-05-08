import React, { Component, Fragment } from 'react';
import './App.css';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast } from 'react-toastify';
import UserSelectPage from './UserSelectPage';
import ProductSelectPage from './ProductSelectPage';
import SummaryPage from './SummaryPage';

class App extends Component {
  constructor() {
    super();
    this.state = {
      stage: 'user',
      user: null,
      product: null,
    };
  }

  popup = (text, level) => {
    toast[level](text, {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 6000,
    });
  }

  onAdvance = (from, selection) => {
    if (from === 'user') {
      this.setState({
        stage: 'product',
        user: selection,
      });
    } else if (from === 'product') {
      this.setState({
        stage: 'confirm',
        product: selection,
      });
    } else if (from === 'confirm') {
      this.setState({
        stage: 'user',
      });
      const confirmed = selection;
      if (confirmed) {
        this.popup('Tuotteet piikitetty!', 'success');
      } else {
        this.popup('Piikitys peruutettu!', 'warn');
      }
    } else {
      alert('Sivunvaihto kosahti!');
    }
  }

  render() {
    let Page, title;
    const { stage } = this.state;
    if (stage === 'user') {
      Page = UserSelectPage;
      title = 'Kuka olet?';
    } else if (stage === 'product') {
      Page = ProductSelectPage;
      title = 'Mikä tuote?';
    } else if (stage === 'confirm') {
      Page = SummaryPage;
      title = 'Vahvista'
    } else {
      alert('Renderi kosahti!');
    }

    return (
      <Fragment>
        <ToastContainer />
        <div className="App">
          <header className="App-header">
            <h1 className="App-title">{ title }</h1>
          </header>
          <div className="App-header-padder"></div>
          <div className="App-intro">
            <Page info={this.state} advance={selection => this.onAdvance(stage, selection)} />
          </div>
        </div>
      </Fragment>
    );
  }
}

export default App;
