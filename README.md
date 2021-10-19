# KIPA
Convert Kurdish text and words to IPA phonetics.<br>

#### Why to use it?
- Convert texts to IPA with different alternatives 
- Convert numbers to its corresponding Kurdish text
<br>

#### Quick example:
```python
from kipa import kipa

print(kipa.translate_text("Dema we baş be! Ev kîpa ye,
                    \n û ew 1ekemîn mektebe ye
                     ji bo vê mijarê!"))
```
```text
| dɛmɑː wɛ bɑːʃ bɛ |
 ɛv kiːpɑː jɛ |
 uː ɛw jɛkɛkɛmiːn mɛktɛbɛ jɛ ʒɪ boː veː mɪʒɑːɾeː |
```

#### Installation
```shell
pip install kipa
```

#### Usages: 
- To get only the translated text (IPA phonetics text):
```python
import kipa 

ipa_text = kipa.translate_text('SOME_KURDISH_TEXT')
```

- To get an object of the result: 
```python
import kipa 

ipa_text = kipa.get_ipa('SOME_KURDISH_TEXT')
```

- To convert a number to its Kurdish text:
```python
import kipa

number_in_text = kipa.convert(382442)
```
```text
sêsed û heştê û du hezar û çarsed û çil û du
```

<br>
<strong>Note: </strong> Kipa automatically translates the numbers to its corresponding IPA phonetics too.