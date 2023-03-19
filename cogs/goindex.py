import os, discord, config
from fuzzywuzzy import process
from discord.ext import commands


class GoIndex(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def index(self, ctx, *, query: str = None):
        if query is None:
            embed = discord.Embed(
                title="Faber's GoIndex Search",
                description="*in case the [web](https://sd.k-cf.workers.dev/0:/) suck*\n\nusage: `r.index <query>`",
                color=config.embed_color,
            )
            await ctx.reply(embed=embed)
            return
        async with ctx.channel.typing():
            if query.lower() == "vae":
                embed = discord.Embed(
                    title="All SD vaes indexed",
                    description="trinart: [autoencoder_fix_kl-f8-trinart_characters.ckpt](https://sd.k-cf.workers.dev/5:/autoencoder_fix_kl-f8-trinart_characters.ckpt)\n"
                    + "wd 1.4: [kl-f8-anime.ckpt](https://sd.k-cf.workers.dev/5:/kl-f8-anime.ckpt)\n"
                    + "wd 1.4: [kl-f8-anime2.ckpt](https://sd.k-cf.workers.dev/5:/kl-f8-anime2.ckpt)\n"
                    + "novelai: [novelai.ckpt](https://sd.k-cf.workers.dev/5:/novelai.ckpt)\n"
                    + "sd 1.5: [vae-ft-ema-560000-ema-pruned.ckpt](https://sd.k-cf.workers.dev/5:/vae-ft-ema-560000-ema-pruned.ckpt)\n"
                    + "sd 1.5: [vae-ft-mse-840000-ema-pruned.ckpt](https://sd.k-cf.workers.dev/5:/vae-ft-mse-840000-ema-pruned.ckpt)",
                    color=config.embed_color,
                )
                await ctx.reply(embed=embed)
                return
            files = {
                "embeddings": {},
                "hypernetworks": {},
                "lora": {},
                "checkpoints": {},
            }
            files["embeddings"] = self.get_files(
                "Y:/Other computers/My Computer (1)/embeds/embeddings"
            )
            files["hypernetworks"] = self.get_files(
                "Y:/Other computers/My Computer (1)/embeds/hypernetworks"
            )
            files["lora"] = self.get_files(
                "Y:/Other computers/My Computer (1)/embeds/lora"
            )
            files["checkpoints"] = self.get_files(
                "Y:/My Drive/Stable Diffusion/goindex sd/checkpoints"
            )
            # files["vae"] = self.get_files(
            #     "Y:/Other computers/My Computer (1)/embeds/vae"
            # )

            all_files = []
            for _type in files:
                for file in files[_type]:
                    all_files.append(file)

            res = process.extract(query, all_files, limit=10)
            parsed_res = []
            for re in res:
                if re[1] >= 80:
                    parsed_res.append(re[0])

            final_res = []
            for re in parsed_res:
                for _type in files:
                    for file in files[_type]:
                        if file == re:
                            final_res.append((re, files[_type][re]))

            des = ""
            for re in final_res:
                if "embeddings" in re[1]:
                    des += (
                        "embeddings: ["
                        + re[0]
                        + "]("
                        + re[1]
                        .replace(
                            "Y:/Other computers/My Computer (1)/embeds/embeddings",
                            "https://sd.k-cf.workers.dev/1:/",
                        )
                        .replace(" ", "%20")
                        + ")\n"
                    )
                elif "hypernetworks" in re[1]:
                    des += (
                        "hypernetworks: ["
                        + re[0]
                        + "]("
                        + re[1]
                        .replace(
                            "Y:/Other computers/My Computer (1)/embeds/hypernetworks/",
                            "https://sd.k-cf.workers.dev/2:/",
                        )
                        .replace(" ", "%20")
                        + ")\n"
                    )
                elif "lora" in re[1]:
                    des += (
                        "lora: ["
                        + re[0]
                        + "]("
                        + re[1]
                        .replace(
                            "Y:/Other computers/My Computer (1)/embeds/lora/",
                            "https://sd.k-cf.workers.dev/3:/",
                        )
                        .replace(" ", "%20")
                        + ")\n"
                    )
                elif "checkpoints" in re[1]:
                    des += (
                        "checkpoints: ["
                        + re[0]
                        + "]("
                        + re[1]
                        .replace(
                            "Y:/My Drive/Stable Diffusion/goindex sd/checkpoints/",
                            "https://sd.k-cf.workers.dev/4:/",
                        )
                        .replace(" ", "%20")
                        + ")\n"
                    )
                # elif "vae" in re[1]:
                #     des += (
                #         "vae: ["
                #         + re[0]
                #         + "]("
                #         + re[1]
                #         .replace(
                #             "Y:/Other computers/My Computer (1)/embeds/vae/",
                #             "https://sd.k-cf.workers.dev/5:/",
                #         )
                #         .replace(" ", "%20")
                #         + ")\n"
                #     )
            embed = discord.Embed(
                title="Search query for: " + query,
                description=des,
                color=config.embed_color,
            )
            await ctx.reply(embed=embed)

    def get_files(self, folder: str):
        files = {}
        for root, subdirs, fns in os.walk(folder):
            for fn in fns:
                files[fn] = root.replace("\\", "/") + "/" + fn
        return files


async def setup(client):
    await client.add_cog(GoIndex(client))
