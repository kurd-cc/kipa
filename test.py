from kipa import kipa
import unittest


class TestNumbers(unittest.TestCase):
    def test_convert(self):
        self.assertEqual(kipa.convert(382442), 'sêsed û heştê û du hezar û çarsed û çil û du', 'should be equal')

    def test_ordinal(self):
        self.assertEqual(kipa.get_ordinal(32), 'sî û duyemîn', 'should be equal')

    def test_fraction_simple(self):
        self.assertEqual(kipa.get_fraction('4/5'), 'ji pêncan çar', 'should be equal')

    def test_fraction_one_word(self):
        self.assertEqual(kipa.get_fraction('1/2'), 'nîv', 'should be equal')

    def test_fraction_one_simple_2(self):
        self.assertEqual(kipa.get_fraction('45/12'), 'çil û pênc belavî dwanzdehan', 'should be equal')

    def test_decimal_simple(self):
        self.assertEqual(kipa.get_decimal('34.675', False), 'sî û çar nûqte şeşsed û heftê û pênc', 'should be equal')

    def test_fraction_negative(self):
        self.assertEqual(kipa.get_fraction('-14/22'), 'negatîf ji bîst û duyan çardeh', 'should be equal')

    def test_decimal_negative_complex(self):
        self.assertEqual(kipa.get_decimal('-1.00067', True), 'negatîf yek û ji sed hezaran şêst û heft',
                         'should be equal')

    def test_decimal_long(self):
        self.assertEqual(kipa.get_decimal('-00000000000001.000000000000000067',
                        True), 'negatîf yek nûqte sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir sifir şêst û heft' , 'should be equal')

    def test_fraction_negative_zeros_leading(self):
        self.assertEqual(kipa.get_fraction('-0001/0003'), 'negatîf ji sêyan yek',
                         'should be equal')

    def test_fraction_decimals_negative_zero_leading(self):
        self.assertEqual(kipa.get_fraction(
    '-000.9999/0009.999'), 'negatîf sifir nûqte neh hezar û nehsed û nod û neh belavî neh nûqte nehsed û nod û neh',
                         'should be equal')

    def test_weird_number(self):
        self.assertEqual(kipa.get_fraction(
    '/554/222/2312/123123/321.123/213'), 'belavî pêncsed û pêncî û çar belavî dused û bîst û du belavî du hezar û sêsed û dwanzdeh belavî sed û bîst û sê hezar û sed û bîst û sê belavî sêsed û bîst û yek nûqte sed û bîst û sê belavî dused û sêzdeh',
                         'should be equal')

if __name__ == '__main__':
    unittest.main()