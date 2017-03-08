#include <openssl/bn.h>

int main() {
	BIGNUM* a = BN_new();
	BIGNUM* b = BN_new();
	BIGNUM* n = BN_new();
	BN_dec2bn(&a, "12345678901234567890123456789012345678901234567890");
	BN_dec2bn(&n, "98742135498168543216864656576516168165373218943519");
	BN_CTX* ctx = BN_CTX_new();
	for (int i = 0; i < 16; i++) {
		BN_mod_sqr(b, a, n, ctx);
	}
	return 0;
}
