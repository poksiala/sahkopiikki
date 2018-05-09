import React, { Component, Fragment } from 'react';
import './App.css';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';
import UserSelectPage from './UserSelectPage';
import ProductSelectPage from './ProductSelectPage';
import SummaryPage from './SummaryPage';
import { popup } from './utils';

const TIMEOUT = 60 * 1000; // 60s

class App extends Component {
  constructor() {
    super();
    this.state = {
      stage: 'user',
      user: null,
      product: null,
      timer: null,
    };
  }

  timeout = () => {
    popup('Piikitys aikakatkaistu.', 'warn');
    this.setState({
      stage: 'user',
      user: null,
      product: null,
      timer: null,
    });
  }

  onAdvance = (from, selection) => {
    if (from === 'user') {
      this.setState({
        stage: 'product',
        user: selection,
        timer: window.setTimeout(this.timeout, TIMEOUT),
      });
    } else if (from === 'product') {
      window.clearTimeout(this.state.timer);
      this.setState({
        stage: 'confirm',
        product: selection,
        timer: window.setTimeout(this.timeout, TIMEOUT),
      });
    } else if (from === 'confirm') {
      window.clearTimeout(this.state.timer);
      this.setState({
        stage: 'user',
        timer: null,
        user: null,
        product: null,
      });
      const confirmed = selection;
      if (confirmed) {
        popup('Tuote piikitetty!', 'success');
      } else {
        popup('Piikitys peruutettu!', 'warn');
      }
    } else {
      popup('Sivunvaihto kosahti!', 'error');
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
      popup('Renderi kosahti!', 'error');
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
