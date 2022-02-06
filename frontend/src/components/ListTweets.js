import React from 'react';
import {useState, useEffect} from 'react'
import NewTweet from './NewTweet';

function ListTweets({userSignedIn, authToken}) {
    
    const tweetRestEndpoint = 'tweets'

    const [tweets, setTweets] = useState([])

    useEffect(() => {
        fetch(process.env.REACT_APP_API_URL + tweetRestEndpoint)
          .then(res => res.json()) //TODO - add error handling here
          .then(data => {
            console.log(data)
            setTweets(data)
          })
      }, [])  

  return (
  <div>
      <h3>Tweet Timeline</h3>
      <ul>
      {
        tweets.map((item,ind) => {
          return (<li key={ind}>{item.content}</li>)
        })
      }
      </ul>
      {userSignedIn ? 
        <NewTweet userSignedIn={userSignedIn} authToken={authToken} /> 
        : null}
  </div>
  );
}

export default ListTweets;


