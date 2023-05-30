import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCheck, faX } from '@fortawesome/free-solid-svg-icons'

library.add(faCheck, faX)

export default function Input(props) {
  const inputIcon = <FontAwesomeIcon icon="fa-solid fa-x" className='icon-input' />
  const inputIconValid = <FontAwesomeIcon icon="fa-solid fa-check" className='icon-input-validate' />

  return (
    <div className='div-input'>
      <input
        className='text-input' type={props.type ? props.type : 'text'} placeholder={props.placeholder}
        onChange={props.validate} value={props.value} >
      </input>
      <span className='input-div-icon'>{props.valid ?
        inputIconValid :
        inputIcon
      }
      </span>
    </div>
  )
}