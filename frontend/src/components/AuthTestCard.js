import { useState, useEffect } from 'react';
import React from 'react';

function AuthTestCard({requestObj, authToken}) {
    
    const [data, setData] = useState({})
    
    const options = {
        method: requestObj.method,
        headers: {
            'Content-Type': 'application/json'
        }
    }

    if (requestObj.body) {
        options.body = JSON.stringify(requestObj.body)
    }

    if (requestObj.authToken) {
        options.headers = {
            ...options.headers, 
            'Authorization':` Bearer ${authToken}`
        }
    }

    console.log(options)
    useEffect(() => {
        fetch(requestObj.url, options)
            .then(res => res.json())
            .then(data => {
                setData(data)
                console.log(data)
                
            })
    }, [])

    if (!data) return <h4>Request Pending</h4>

    return (
    <div>
      
        <h3>{requestObj.endpoint}</h3>
        
        <h5>Request</h5>
        
        {   
            Object.entries(requestObj).map(kv => {
                return (<p>
                    <span>{kv[0]}</span>
                    <span> : </span>
                    <span>{JSON.stringify(kv[1])}</span>
                </p>)
            })
        }

        <h5>Response</h5>
        {
            Object.entries(data).map(kv => {
                return (<p>
                    <span>{kv[0]}</span>
                    <span> : </span>
                    <span>{JSON.stringify(kv[1])}</span>
                </p>)
            })
        }

        {/* <p>Method: {data.request_method}</p>
        <p>Response</p>
        dataReturned ? "yes" : "no"
        ((Objects.keys(data.token_data).length > 0) ?
            <div>
            <p>Token expires at   : {data.token_data.exp}</p>
            <p>Token was issued at: {data.token_data.iss}</p>
            </div>
            :
            <p>No Token Data Available</p>) */}

        
    </div>
    )
}

export default AuthTestCard;
