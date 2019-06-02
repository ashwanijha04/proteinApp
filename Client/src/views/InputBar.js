import React from "react";
import { Form, FormGroup} from 'reactstrap';
import ReactLoading from "react-loading";
import classnames from "classnames";
import { Button, Modal, Label, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

import {
  Input,
  InputGroup,
  InputGroupAddon,
  InputGroupText,
  Card,
  CardBody
} from "reactstrap";

const url = "http://localhost:5000/app";

const Note = ({note}, {idx}) => (
    <div>
        <p> {note} </p>
    </div>
);

class InputBar extends React.Component {
  constructor() {
  super();
  this.state = {
    note: '',
    notes: [],
    visible: false,
    focused: "",
    formModal: false

  };
  this.startLoading = this.startLoading.bind(this);
  this.stopLoading = this.stopLoading.bind(this);


}

toggleModalSVM = modalState => {
  this.startLoading()

  setTimeout(() => {
    this.setState({
      [modalState]: !this.state[modalState]
    });
  }, 6000)


  setTimeout(() => {
    this.stopLoading()
  }, 6000)


};

toggleModalFold = modalState => {
  this.startLoading()

  setTimeout(() => {
    this.setState({
      [modalState]: !this.state[modalState]
    });
  }, 1000)


  setTimeout(() => {
    this.stopLoading()
  }, 1000)


};

toggleModalNN = modalState => {
  this.startLoading()

  setTimeout(() => {
    this.setState({
      [modalState]: !this.state[modalState]
    });
  }, 3000)


  setTimeout(() => {
    this.stopLoading()
  }, 3000)


};

closeModal = modalState => {

  this.setState({
    [modalState]: !this.state[modalState]
  });
}


onFocus = () => {
  this.setState({
    focused: "input-group-focus"
  });
};
onBlur = () => {
  this.setState({
    focused: ""
  });
};

startLoading() {
   // setTimeout(() => {
   //  this.setState({visible: !this.state.visible})
   // }, 2000)
      this.setState({visible: true})
   }

stopLoading() {
  // setTimeout(() => {
  //  this.setState({visible: !this.state.visible})
  // }, 2000)
     this.setState({visible: false})
  }

componentDidMount() {
  const api_url = '/predict';
  fetch(api_url)
    .then(response => response.json())
    .then(
      data => this.setState({
      notes: data
    },

    (error) =>{
      console.log("Error");
    }

  ))}

_handleChange = (event) => {
  const state = this.state;
  state[event.target.name] = event.target.value;
  this.setState(state);
}

_handleSubmit = (event)  => {
  event.preventDefault();
  const {note} = this.state;
  const api_url = '/predict';
  const options = {
    method: 'POST',
    body: JSON.stringify({
      note: note
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  };

  fetch(api_url, options)
    .then(response => response.json())
    .then(data => {
      this.setState({
        note: '',
        notes: data
      }
    )
    })
    .catch(error => console.log(error));


}


  render() {
    return (
      <div className="sequence-class">


      <div>

    <form onSubmit={this._handleSubmit}>
       <Card>
         <CardBody>
         <InputGroup className={this.state.focused}>
            <InputGroupAddon addonType="prepend">
               <InputGroupText><i className="fas fa-brain"></i></InputGroupText>
             </InputGroupAddon>
               <Input className="input-class"
                 type="text"
                 name="note"
                 placeholder="Amino-acid Sequence"
                 onFocus={this.onFocus}
                 onBlur={this.onBlur}
                 value={this.state.note}
                 onChange={(event)=>this._handleChange(event)}
               />
           </InputGroup>
         </CardBody>
       </Card>



      <Button align="center" name="button" onClick={() => this.toggleModalSVM("formModal")} color="default" type="submit">SVM </Button>
      <Button align="center" name="button" onClick={() => this.toggleModalFold("formModal")} color="danger" type="submit">Fold Algorithm</Button>
      <Button align="center" name="button" onClick={() => this.toggleModalNN("formModal")} color="alert" type="submit">Neural Network </Button>

      <br/>
      <a target="_blank" href="https://npsa-prabi.ibcp.fr/cgi-bin/npsa_automat.pl?page=/NPSAHLP/npsahlp_sequence.html"> HELP </a>

    </form>
    </div>


       {this.state.visible &&
         <div align="center">

         <ReactLoading color="#FFFFFF" type={"cylon"}/>

         </div>}





        <div>
        <Modal
          modalClassName="modal-black"
          isOpen={this.state.formModal}
          toggle={() => this.toggleModal("formModal")}
        >
          <div className="modal-header justify-content-center">
            <button
              className="close"
              onClick={() => this.toggleModal("formModal")}
            >
              <i className="tim-icons icon-simple-remove text-white" />
            </button>
            <div className="text-muted text-center ml-auto mr-auto">
              <h3 className="mb-0">Results</h3>
            </div>
          </div>
          <div className="modal-body">
             {/* To get started, edit <code>src/App.js</code> and save to reload. */}

             {
               Object.keys(this.state.notes).map((idx) => {
                 return <Note key={idx} note={this.state.notes[idx]} />
               })
             }





              <div className="text-center">
                <Button className="my-4" color="primary" type="button" onClick={() => this.closeModal("formModal")}>
                  Awesome!
                </Button>
              </div>
          </div>
        </Modal>
        </div>

        {this.props.children}
      </div>
    );
  }
};


export default InputBar;
