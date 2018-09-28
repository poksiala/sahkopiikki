import 'whatwg-fetch';
import React, { Component } from 'react';
import qs from 'qs';
import './App.css';

const ErrorContainer = ({error}) => (
  <div className="App-error">
    { String(error) }
  </div>
);

const get = async (url, data) => {
  const token = qs.parse(window.location.search.split('?')[1]).token;
  const headers = {
    'Authorization': `Token ${token}`,
  };
  const init = {
    method: 'GET',
    headers,
    mode: 'cors', // no-cors, cors, *same-origin
    redirect: 'follow', // manual, *follow, error
    referrer: 'no-referrer', // *client, no-referrer
    cache: 'no-cache',
  };

  let resp;
  try {
    resp = await fetch(url, init);
  } catch (err) {
    console.log(err);
    throw new Error(`Cannot GET from url: ${url}. See log for details.`);
  }

  if (!resp.ok) {
    if (resp.status === 401) {
      throw new Error(`Unauthorized. Did you remember the token?`);
    } else {
      throw new Error(`GET returned status ${resp.status}`);
    }
  }

  let json;
  try {
    json = await resp.json();
  } catch (err) {
    console.log(err);
    throw new Error(`Cannot parse JSON from GET. See log for details.`);
  }

  return json;
}

class Fetcher extends Component {
  constructor(props) {
    super(props);
    this.state = {
      ready: false,
      data: null,
      error: null,
    };

    this.fetchData = this.fetchData.bind(this);
    this.fetchData(props.url).catch(err => {
      this.setState({
        ready: false,
        error: err,
      })
    });
  }

  async fetchData(url) {
    const json = await get(url);

    this.setState({
      data: json,
      ready: true,
      error: null,
    });
  }

  render() {
    const { ready, error, data } = this.state;
    if (ready) {
      return React.cloneElement(this.props.children, { data, });
    } else if (error) {
      return <ErrorContainer error={error} />
    } else {
      return null;
    }
  }
}

const POST_THROTTLE_MS = 1000;
let lastPostTimestamp = Date.now();

const post = async (url, data) => {
  const token = qs.parse(window.location.search.split('?')[1]).token;
  const headers = {
    'Authorization': `Token ${token}`,
    'content-type': 'application/json'
  };
  const init = {
    method: 'POST',
    headers,
    body: JSON.stringify(data),
    mode: 'cors', // no-cors, cors, *same-origin
    redirect: 'follow', // manual, *follow, error
    referrer: 'no-referrer', // *client, no-referrer
    cache: 'no-cache',
  };

  const now = Date.now();
  if (now - lastPostTimestamp < POST_THROTTLE_MS) {
    console.warn('Throttled POST request in frontend.');
    const err = new Error('Throttled POST request in frontend.');
    err.throttled = true;
    throw err;
  }

  lastPostTimestamp = now;

  let resp;
  try {
    resp = await fetch(url, init);
  } catch (err) {
    console.log(err);
    throw new Error(`Cannot POST to url: ${url}. See log for details.`);
  }

  if (!resp.ok) {
    if (resp.status === 401) {
      throw new Error(`Unauthorized. Did you remember the token?`);
    } else {
      throw new Error(`POST returned status ${resp.status}`);
    }
  }

  let json;
  try {
    json = await resp.json();
  } catch (err) {
    console.log(err);
    throw new Error(`Cannot parse JSON from POST response. See log for details.`);
  }

  return json;
};

export { get, post };
export default Fetcher;