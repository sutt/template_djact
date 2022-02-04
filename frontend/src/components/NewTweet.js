import React from 'react';
import { useState } from "react";

function NewTweet({userSignedIn, authToken}) {

  const endpoint = 'tweets/'

  const [formInfo, setFromInfo] = useState(
    {
      username: userSignedIn, 
      content: '',
    }
  )

  const [networkErrMsg, setNetworkErrMsg] = useState(null)
  const [clientErrMsg, setClientErrMsg] = useState(null)

  const statusCodeToErr = (responseObj) => {
      setNetworkErrMsg(`Network Error of code: ${responseObj.status}`)
      // TODO - console log the err message
  }

  const clientFormValidation = (formInfo) => {
      const blankFields = Object.entries(formInfo)
                                .filter(kv => kv[1] === '')
      if (blankFields.length > 0) {
          setClientErrMsg(`${blankFields[0][0]} can not be blank`)
          return false
      }
      setClientErrMsg(null)
      return true
  }

  const handleChange = (e) => {
      setFromInfo({...formInfo, [e.target.id]: e.target.value})
  }

  const handleSubmit = (e) => {
      
      // console.log(formInfo)
      e.preventDefault()

      setNetworkErrMsg(null)

      if (!clientFormValidation(formInfo)) {
          return
      }
      
      const apiUrl = process.env.REACT_APP_API_URL
      
      console.log(`fetching with token ${authToken}`)
      
      fetch( apiUrl + endpoint,       
              {
                  method: 'POST',
                  headers: {
                      'Content-Type':'application/json',
                      'Authorization':` Bearer ${authToken}`
                  },
                  body: JSON.stringify(formInfo)
              }
      )
          .then(res => {
              if (res.ok) {
                  return res.json()
              } else {
                  statusCodeToErr(res)
                  return Promise.resolve(null)
              }
          })
          .then(data => {
              if (!data) {
                  console.log(`problem with network request: ${networkErrMsg}`)
              } else {
                  
                  console.log(data)

                  // call to refresh the list
                  // set RefreshCounter(refreshCounter + 1)
              }
          })
  }

    
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input id="content" type="text" onChange={handleChange}/>
                <button type="submit">Tweet It</button>
            </form>
            <p>{networkErrMsg}</p>
            <p>{clientErrMsg}</p>
        </div>
  )
}

export default NewTweet;
