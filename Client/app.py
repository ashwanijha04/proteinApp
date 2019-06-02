import json
from flask import Flask, request, Response, jsonify
import sys
import pickle
import pandas as pd
import numpy as np
import ast

from py4j.java_gateway import JavaGateway
from py4j.java_gateway import GatewayParameters
#sys.path.insert(0, '/Users/ashwajha/Desktop/ReactApp')
invalid_list = ['GTCGACCTGCAGGGCGAAGGCGTTTTCGCCAAGTTCGGCGACCAGTTTGTTGAGCTTTTC']


app = Flask(__name__)


import pickle
import pandas as pd
import numpy as np
import keras

#pickle_in = open("/Users/autkarsh/Desktop/ProteinApp/wrapper-funcs/resRnet/finalized_model.sav","rb")




def ResNetAlgo(sequence):

    if(sequence in invalid_list):
        return "The sequence doesn't look like a proteic one. Let's try again."



    df = pd.read_csv("/Users/ashwajha/Downloads/FeatureVectors.csv")

    filename = "/Users/ashwajha/Desktop/Protein Structure Prediction/ReactApp/dict.pickle"
    with open(filename, 'rb') as f:
        model = pickle.load(f)
#    model = pickle.load(pickle_in)

    seq = {}
    seq= df.sample()
    classes = []
    classes.append("Alpha Helix")
    classes.append("Random Coil")
    classes.append("Extended Strand")
    #print(classes[0])

    #seq = [0.32467532,0.37662336,0.2987013,0.3181818,0.37012988,0.3116883,0.3181818,0.2792208,0.4025974,0.29220778,0.3961039,0.3116883,0.14285715,0.09090909,0.11038961,0.16233766,0.12337662,0.103896104,0.077922076,0.14285715]


    gateway = JavaGateway(gateway_parameters=GatewayParameters(port=25335))
    #seq = 'MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG'
    s1=gateway.entry_point.showmssg(sequence)
    #msg =s1.showmssg()
    print(s1,type(s1))
    s2 = ast.literal_eval(s1)
    print(s2,type(s2))
    #s3 = [0.32467532,0.37662336,0.2987013,0.3181818,0.37012988,0.3116883,0.3181818,0.2792208,0.4025974,0.29220778,0.3961039,0.3116883,0.14285715,0.09090909,0.11038961,0.16233766,0.12337662,0.103896104,0.077922076,0.14285715,0.14285715,0.14285715,0.12337662,0.103896104,0.0,0.26623377,0.5,0.78571427,0.987013,0.0,0.32467532,0.5649351,0.76623374,0.9935065,0.0,0.17532468,0.43506494,0.6883117,0.96753246,0.0,0.2792208,0.512987,0.77922076,0.9935065,0.0,0.18181819,0.44155845,0.7012987,0.987013,0.0,0.2857143,0.5194805,0.75974023,0.9805195,0.0,0.18181819,0.44155845,0.71428573,0.987013,0.0,0.32467532,0.53896105,0.77922076,0.9935065,0.0,0.26623377,0.5064935,0.7467533,0.96753246,0.0,0.2792208,0.47402596,0.7987013,0.9935065,0.0,0.18831168,0.46103895,0.7012987,0.987013,0.0,0.2857143,0.5194805,0.75974023,0.9805195,0.025974026,0.12337662,0.09090909,0.038961038,0.032467533,0.012987013,0.071428575,0.116883114,0.038961038,0.032467533,0.025974026,0.071428575,0.019480519,0.0,0.051948052,0.116883114,0.058441557,0.019480519,0.038961038,0.012987013,154.0]
    seq1 = np.array(s2)
    seq1 = seq1.reshape(1,-1)
    result = model.predict(seq1)
    idx = np.argmax(result)
    print(result)
    print(classes[idx])
    print(model.predict(seq1))

    return ("The predicted structure is : " + str(result[0]))



#ResNetAlgo('MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG')
notes = {

}

#def findString(s):
#    str = s

@app.route('/predict', methods=['GET', 'POST'])
def serve():
    i=0
    if request.method == 'POST' and request.is_json:
        new_note = request.get_json()['note']
        print(type(new_note))
        new_note_id = len(notes)
        #notes[i] = (new_note)
        #i = i + 1
        structure = ResNetAlgo(str(new_note))
        notes[i]=(structure)
        #i= i+1
        print(new_note)
        print(structure)

    return Response(

        json.dumps(notes),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

"""@app.route('/api/v1/notes', methods=['POST'])
def serve_again():
    return Response(

        json.dumps({
            "Accuracy": accuracy,
            "sequence": str
            }
        ),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )"""


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True)
