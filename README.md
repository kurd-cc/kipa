# KIPA
Convert Kurdish text and words to IPA phonetics.<br>

#### Why to use it?
- Convert texts to IPA with different alternatives 
- Convert numbers to its corresponding Kurdish text
- It prioritizes the word's sound in the Kurdish Wiktionary (Wikiferheng) and return the generalized one if it doesn't exist.
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
number_ordinal = kipa.get_ordinal(32)
normal_fraction = kipa.get_fraction('4/5')
fraction_has_name = kipa.get_fraction('1/2')
numerator_bigger_than_denominator = kipa.get_fraction('45/12')
decimal_simple = kipa.get_decimal('34.675', False)
decimal_complex = kipa.get_decimal('34.675', False)
negative_fraction = kipa.get_fraction('-14/22')
negative_complex_decimal = kipa.get_decimal('-1.00067', True)
negaive_weird_decimal = kipa.get_decimal('-00000000000001.000000000000000067', True)
negative_weird_fraction = kipa.get_fraction('-0001/0003')
```
```text
sêsed û heştê û du hezar û çarsed û çil û du
sî û duyemîn
ji pêncan çar
nîv
çil û pênc belavî dwanzdehan
sî û çar nûqte şeşsed û heftê û pênc
sî û çar û ji hezaran şeşsed û heftê û pênc
negatîf ji bîst û duan çardeh
negatîf yek û ji sed hezaran şêst û heft
negatîf yek nûqte sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir şêst û heft
negatîf ji sêyan yek
```

<br>
<strong>Note: </strong> Kipa automatically translates the numbers to its corresponding IPA phonetics too.