import os
import numpy as np
import tensorflow as tf
from dante_by_syl.data_preparation import text_in_syls
from dante_by_syl.text_processing import prettify_text, special_tokens

def generate_text(model, special_tokens, vocab_size, syl2idx, idx2syl, seq_length, single_output, start_string, temperature=1.0):
    generated_text = start_string.replace(' ', '').replace('\n','')
    print(prettify_text(generated_text, special_tokens), end='', flush=True)
#    sequence = start_string
    sequence = [ syl2idx[syl] for syl in text_in_syls(start_string)[-seq_length:] ]
    prediction = ''
    model.reset_states()
    i = 0
    while prediction != special_tokens['END_OF_CANTO'] \
            and generated_text.count(special_tokens['START_OF_TERZINA']) < 45 \
            and generated_text.count(special_tokens['END_OF_VERSO']) < 136 \
            and i < 700:
        
#        sequence = [ syl2idx[syl] for syl in text_in_syls(generated_text)[-seq_length:] ]
        sequence = tf.keras.preprocessing.sequence.pad_sequences([sequence], maxlen=seq_length)
        x = np.array(sequence, dtype='int64')
#        print(x)

        prediction = model.predict(x, verbose=0)
        
        if single_output:
            prediction = tf.squeeze(prediction, 0)
        else:
            prediction = tf.squeeze(prediction, 0)[-1]
        prediction = prediction / temperature
#        prediction = tf.nn.softmax(prediction).numpy()
#        prediction /= np.sum(prediction)
        prediction = prediction.numpy()
        index = np.random.choice(len(prediction), size=1, p=prediction)[0]

#        index = np.argmax(prediction)


#        prediction = model.predict(x, verbose=0)
#        prediction = tf.squeeze(prediction, 0)
#        prediction = prediction / temperature
#        index = tf.random.categorical(prediction, num_samples=1)[-1,0].numpy()

        prediction = idx2syl[index]
        generated_text += prediction
        sequence = sequence[1:] + [index]

#        print(prediction, end='', flush=True)
        print(prettify_text(prediction, special_tokens), end='', flush=True)
        i+=1        
    print('\n')        
    return generated_text


