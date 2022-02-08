import React, {useEffect, useState} from 'react';

function Profile({userSignedIn, authToken}) {
  
    const profileEndpoint = 'list_profile_tweets'
    // const profileEndpoint = 'list_profile_tweets_serialized'
    
    const [networkErrMsg, setNetworkErrMsg] = useState(null)

    const [userData, setUserData] = useState(
        {
            userTweets:[],
            userName: userSignedIn,
        }
    )

    const statusCodeToErr = (responseObj) => {
        setNetworkErrMsg(`Network Error of code: ${responseObj.status}`)
        // TODO - console log the err message
    }

    useEffect(() => {
        
        fetch( process.env.REACT_APP_API_URL + profileEndpoint,       
            {
                method: 'GET',
                headers: {
                    'Content-Type':'application/json',
                    'Authorization':` Bearer ${authToken}`
                },                
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
                    
                    const tmpUserData = {
                        userTweets: data,
                        userName: userSignedIn,
                    }
                    
                    setUserData(tmpUserData)
  
                }
            })

    }, [])
  
    return (
    <div>
        <h3>{userSignedIn}'s Tweets:</h3>
        {
            userData.userTweets.map((item, ind) => {
                return (<li key={ind}>{item.content}</li>)
            })
        }

    </div>
    )
}

export default Profile;
