import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTrash, faEdit } from '@fortawesome/free-solid-svg-icons'

library.add(faTrash, faEdit)


export default function PwdCard(props) {
  const [getToken, setToken] = useState(sessionStorage.getItem('token'));

  function delete_pwd() {
    let url = `http://127.0.0.1:8000/pwd/del/`
    const formData = new FormData();
    formData.append('title', props.data.title)

    let data = {
      method: 'DELETE',
      headers: { Authorization: 'Token ' + getToken },
      body: formData
    }
    fetch(url, data)
      .then(props.update)
  }


  return (
    <div className="pwd-card">
      <a className="pwd-title"> {props.data.title} </a>
      <div className='align-btns'>
        <button className='pwd-del' onClick={props.edit}> <FontAwesomeIcon icon="fa-solid fa-edit" /> </button>
        <button className='pwd-del' onClick={delete_pwd}> <FontAwesomeIcon icon="fa-solid fa-trash" /> </button>
      </div>
    </div>
  )
}