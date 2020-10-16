import os
import numpy as np
import tensorflow as tf

def generate_text(model, special_tokens, vocab_size, char2idx, idx2char, seq_length, start_string, temperature=1.0):
    generated_text = start_string
    sequence = start_string
    prediction = ''
    model.reset_states()
    i = 0
    while prediction != special_tokens['END_OF_CANTO'] \
            and generated_text.count(special_tokens['START_OF_TERZINA']) < 45 \
            and generated_text.count(special_tokens['END_OF_VERSO']) < 136 \
            and i < 1500:
        
        sequence = [ char2idx[ch] for ch in generated_text[-seq_length:] ]
        sequence = tf.keras.preprocessing.sequence.pad_sequences([sequence], maxlen=seq_length)
        x = np.array(sequence, dtype='int64')
#        print(x)

        prediction = model.predict(x, verbose=0)
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

        prediction = idx2char[index]
        generated_text += prediction
#        sequence = sequence[1:] + prediction

        print(prediction, end='', flush=True)
        i+=1        
    print('\n')        
    return generated_text

