import discord  # type: ignore
from discord.ext import commands  # type: ignore

import requests
from database_manager import insert_profile

uuids = ['23331ef9edaa4e1fa71baa82bb1982c2', '4085ff0af28d4534bf325decb14376d5', '9648b72eeff6446588b13ce079c647a8', '130b3075c7b84ce0a016034c3a1d7bee', '2ed4b01e4f394d09b7ed66fcdfc3f727', 'c94f9e8412f94cfc88c06a1c6df3b0b5', '1545500448444122a9b750c1a856fb8c', '7c326e8b9a5a45b785ac79b110d718e3', '4fe0fdbfa5c6443e914ee786471f2453', '19605973f2554786af16e79692c4c4d1', '22fb74ab817945ffaefb23350b81487a', '4603e44959d24d1daf554b313b343f88', 'a68ae683e1684d49baf0966bf2537f5e', '9de64e171d034155b61f3f3056e69089', 'c672eed314f84dcaa0c6f74a5a52c8f2', '7da8f127c7b549eb9fd33f37b95252ac', 'a1c421ff5e024f75b1a46c30ca68c749', '773a891bd0ea44e583f487280892f439', 'ab4c7896b5c24d1fa60aad904b1fb6bb', '6e90365c2dc9458e97ce08534352e2a1', '6275c006ce154abc8143adc549ef76bb', '6fd1d52fcb0f4d97b8d84542f93f2658', 'b451e21fafda403f983da3842a55ab67', 'dd959a35c6d74ae28b9a7fcb9434637c', '1277d71f338046e298d90c9fe4055f00', '28667672039044989b0019b14a2c34d6', '529dabfd5b154d90b105a3a81da2c525', 'e23e44f605f24f23b65e51b449dd0c0d', 'fb3d96498a5b4d5b91b763db14b195ad', 'fa0ea97de33443d6b5045f18229a154b', '96b04cd0f41c4752801cc9baea6da892', '04cd3f240c7f42009b3398fba995c3a6', '4f562091f4614f659546717d6bbdfe79', '0291afe06e36412ab88cacafb74e1cd6', '88fec3c939904ec8a07890f342253d4d', '99f50870447c4e508c95086048a7f196', '39d7c75b5fbf437c8e853d58934c2d2b', 'd35de691f4ca4cc2bfe40f372f04a6e4', '885c77cebb29471b95e3516d1118bc76', '84deddf1f0c442079716f501b11db173', 'b3e7ed8fd4144e02a85c1a86d4012807', '0625fd8f36d746eeb7cb6a0972c0df0d', 'a05ac4b9445041fa8f29e3ea117958ad', '6329d4d93f04421ab95d356086fce83c', 'f1608634ce8a4e1c9645511069f59487', '78926764ee53437b91d96dbf2b3b1dca', '78acba393ce149f68855f9bca5907432', '6011e893c45542629c7c8cc94bd88a35', '5a9df7ad49aa4747939130efc3cd6cea', '5c6d8f6645b24a5ca37970053ffd32d6', '29135e50c229404ba0b2a147abc374fc', '236f99cc5439455cb10aa29c3202082e', 'c713e1ef28844ceaaac306c44e39505f', 'f5d20b3123b345b1a46cc9eb5a413d19', '6de0b8b24d8548e8ab1b545322909aee', '5435b597612f4554a3c651fd1c3ee96a', '1cb36e3f0b0742ea8abe396a70d234a4', '6808325e8d44418ca34b61e22471e5a7', 'e8ff41bc06b3449cbff3107e90309497', '2e9971217d894aa9beff00434843fe07', '4fef66aace5641b6b4b2bf272d765d9f', '29baf21ea788440da3f132b0a1ab01c3', 'd472f48813c941148c5a3c360e87c40b', '8a7ce3df6a4b4befad4e42028efe19cc', '90905cf347be483dbac440a6e631bc91', '41eb2439084e4233bab9b6defd7749fb', '973dc5a4f604489eb350aff3a07228a1', '9dad65f5d0ce4f6e83ff23ce676af28f', '86a7793c061743deb2e4894a5d2e5ccd', '66cb6384bbce477c854b815548458224', 'c558970dca7343a79083825bacfa65c7', 'cd5aa0c479394e8b812d1a755e450ef8', '9a5624746131475ea213b97f4d5e23a9', 'a68c92d3963942e3b1c695241fcfa2c0', '4ce231a79af8473faf1dab7ecf4de2ad', 'c0a5e970db87492e93c260f8221d1c98', '53ded400553046c694605f167df88366', '5ad6ed71fb17453c8e367cc66e8b6982', '3ffc65982a904193a8e17f241ddef6cd', '88687e0e24d940229868279d55616c26', 'b7ed1e5f6c624b57a21fa66f3b4e297a', '58e7ba62ed31445c8fa71cf5ed575940', '6f34fab4b6fe4522b215fa01ae68f412', 'd6b5d5120ef0409698ee2ad30754c7d2', '919e74ebf227422ea94719cb7273b03b', 'ded0c8298a9b4db0819822256a3eccb0', '6994c547f53e4107ace4a0bb48609bb5', '8cac680761a7412b91b306f489a5871f', '637c355ef3fc4eeb88c2a7c18c0bf815', 'dd5818337cf545e6b834ff1644b76cca', '311b651b782844a0a0889130922434ca', '2d17608169d844d0b8d828df1438dbfb', 'f5cddb7611cc45659e25448022ef81a1', '073a5abb4b734339a1e90ef43d504842', 'c00cc747e84340ddbf76374651b34c0b', 'c714874fdb594844b24f1f0c3b63408f', '7903f5c3631244ae9bc16018feb38b43', '23467d4464474adfb77c1e5a044e5e5b', 'f8afcbe455d242e1aaa6722d3ed110bc', '4995579a28f647dfbc03f33fd2aec058']

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY = file.read()

class populate_leaderboard_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.is_owner()
    @commands.command(aliases=["pl"])
    async def populate_leaderboard(self, ctx) -> None:        

        for uuid in uuids:
            print(f"Re-calculated {uuid}")
            profile_data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
            
            request = requests.post(f"http://{self.client.ip_address}:8000/pages/{uuid}", json=profile_data)
            if request.status_code != 200:
                continue
            
            request_data = request.json()

            data_totals = [request_data.get(page, {"total": 0})['total'] for page in ("purse", "banking", "inventory", "accessories", "ender_chest", "armor", "vault", "wardrobe", "storage", "pets")]
            insert_profile(uuid, request_data["profile_data"]["profile_name"], request_data["profile_data"]["profile_type"], *data_totals)

