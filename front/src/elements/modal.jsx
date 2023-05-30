import { useState, useEffect } from "react";
import Input from "./input";


export default function Modal(props) {
  const [getToken, setToken] = useState(sessionStorage.getItem('token'));

  // inputs
  const [getTitle, setTitle] = useState("");
  const [getUser, setUser] = useState("");
  const [getUrl, setUrl] = useState("");
  const [getPwd, setPwd] = useState("");

  // validate
  const [getTitleValid, setTitleValid] = useState("");
  const [getPwdValid, setPwdValid] = useState("");

  function close_modal() {
    const modal = document.getElementById("ModalNew");
    modal.classList.remove("show");
  }

  function validate_form() {
    if (getPwdValid && getTitleValid) {
      new_pwd()
    } else {
      const tip = document.getElementById("modalTip")
      tip.innerText = "Prencha os dados corretamente"
    }
  }

  function create_form() {
    const formData = new FormData();
    formData.append("title", props.data?.title);
    formData.append("new_title", getTitle)
    formData.append("user", getUser)
    formData.append("url", getUrl)
    formData.append("pwd", getPwd)
    return formData
  }

  function new_pwd() {
    let url = props.save ? "http://127.0.0.1:8000/pwd/new/" : "http://127.0.0.1:8000/pwd/edit/"
    const formData = create_form()
    let data = {
      method: 'POST',
      headers: { Authorization: 'Token ' + getToken },
      body: formData
    }
    fetch(url, data)
      .then(() => {
        close_modal()
        props.update()
      })
  }

  // Validates
  const validate_title = (event) => {
    const value = event.target.value
    if (value) {
      setTitleValid(true)
      setTitle(value)
    } else {
      setTitleValid(false)
      setTitle(value)
    }
  }

  const validate_pwd = (event) => {
    const value = event.target.value
    if (value) {
      setPwdValid(true)
      setPwd(value)
    } else {
      setPwdValid(false)
      setPwd(value)
    }
  }

  const validate_user = (event) => {
    const value = event.target.value
    setUser(value)
  }

  const validate_url = (event) => {
    const value = event.target.value
    setUrl(value)
  }

  useEffect(() => {
    const fakeTitle = { target: { value: props.data.title || '' } };
    setTitle(props.data?.title || "")
    validate_title(fakeTitle)

    const fakePwd = { target: { value: props.data.pwd || '' } };
    setPwd(props.data?.pwd || "")
    validate_pwd(fakePwd)

    setUser(props.data?.user || "")
    setUrl(props.data?.url || "")
    const tip = document.getElementById("modalTip")
    tip.innerText = ""
  }, [props.data])

  return (
    <div className="modal-background" id="ModalNew" onClick={close_modal}>
      <div className="modal-div" onClick={e => e.stopPropagation()}>
        <div className="align-inputs">
          <Input className="text-input" placeholder="Digite o titulo da senha" valid={getTitleValid}
            validate={validate_title} value={getTitle}>
          </Input>

          <Input className="text-input" placeholder="Digite o usuario" valid={true}
            value={getUser} validate={validate_user}>
          </Input>

          <Input className="text-input" placeholder="Digite a url" valid={true}
            value={getUrl} validate={validate_url}>
          </Input>

          <Input className="text-input" placeholder="Digite a sua senha" valid={getPwdValid}
            validate={validate_pwd} value={getPwd}>
          </Input>
        </div>
        <div className='align-btns'>
          <button className='btn' onClick={validate_form}> Salvar </button>
        </div>
        <br></br>
        <a className='login-tip' id='modalTip'> </a>
      </div>
    </div>
  )
}