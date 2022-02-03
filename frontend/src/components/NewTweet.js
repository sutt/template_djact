import React from 'react';

function NewTweet() {
  
    const handleSubmit = (e) => {
      e.preventDefault()
      alert(`feature not implemented yet`)
    }
    
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input id="content" type="text"/>
                <button type="submit">Tweet It</button>
            </form>
        </div>
  )
}

export default NewTweet;
