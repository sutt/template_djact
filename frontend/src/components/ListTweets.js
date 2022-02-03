import React from 'react';
import {useState, useEffect} from 'react'
import NewTweet from './NewTweet';

function ListTweets({userSignedIn}) {
    
    const tweetRestEndpoint = 'tweets'

    const [tweets, setTweets] = useState([])

    useEffect(() => {
        fetch(process.env.REACT_APP_API_URL + tweetRestEndpoint)
          .then(res => res.json())
          .then(data => {
            console.log(data)
            setTweets(data)
          })
      }, [])  

  return (
  <div>
      <h1>Tweet Timeline</h1>
      <ul>
      {
        tweets.map((item,ind) => {
          return (<li key={ind}>{item.content}</li>)
        })
      }
      </ul>
      {userSignedIn ? <NewTweet/> : null}
  </div>
  );
}

export default ListTweets;

