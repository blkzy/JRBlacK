from Commands.Utils.icons import getIcon
from Commands.Utils.check import checks
from discord.ext import commands
from datetime import datetime
from Database import *

import discord
import random

PersonI   = getIcon("Receiver")
TransferI = getIcon("Transfer")
ExtractI  = getIcon("Extract")
DepositI  = getIcon("Deposit")
WalletI   = getIcon("Wallet")
MoneyI    = getIcon("Money")
NameI     = getIcon("Name")
BankI     = getIcon("Bank")
RankI     = getIcon("Rank")
AtmI      = getIcon("Atm")
IdI       = getIcon("ID")

"""class economy(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.Guild    = database.Guild()
        self.GuildGet = database.GuildGet()
        self.User     = database.User()
        self.user. = database.UserPost()
        self.user.  = database.UserGet()

    async def withdrawMoney(self, guild, member, money):

    async def depositMoney(self, guild, member, money):"""

class MyBank(commands.Cog, name="Banco"):
    def __init__(self, client):
        self.client = client
        self.check = database.check()
        self.guild = database.guild()
        self.user  = database.user()

    async def sub_commands(self, ctx, command):
        lista = []
        for x in self.client.get_command(command).all_commands:
            if self.client.get_command(f'{command} {x}').name is x:
                lista.append(x)

        x = "".join(lista)
        if len(lista) > 1:
            x = " | ".join(lista)

        return await ctx.send(f"""```asciidoc
[Comando {command}]
  Modo de uso    :: {self.client.get_command(command).usage}
  Sub Comando(s) :: {x}
```""")

    @commands.group(name="banco", aliases=["bank"], no_pm=True, usage="[p]banco [sub command]")
    async def _bank(self, ctx):
        if self.guild.get_systemEconomy(ctx.guild.id) == 'True':
            if not self.check.user(ctx.guild.id, ctx.author.id):
                self.user.create(ctx.guild.id, ctx.author.id)

        if ctx.invoked_subcommand is None:
            if self.guild.get_whitelist(ctx.guild.id) == ctx.channel.id or self.guild.get_whitelist(ctx.guild.id) == 0:
                return await self.sub_commands(ctx, ctx.command.name)
            else:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027), delete_after=15)

    @commands.check(checks.whitelist)
    @commands.cooldown(1, 54000, commands.BucketType.member)
    @_bank.command(aliases=['diariamente', 'salario'], no_pm=True, usage="[p]banco daily")
    async def daily(self, ctx):
        if self.check.guild(ctx.guild.id) is False:
            return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você precisa configurar o servidor na database.", color=0xef0027))
            
        if self.guild.get_systemEconomy(ctx.guild.id) == 'False':
            return await ctx.send(embed=discord.Embed(description=f"{BankI} Sistema de economia está desativado neste grupo.", color=0xef0027).set_footer(text="Para tivar use o comando: [p]set economy"))

        valores = '1234567890'
        d = (f'{random.choice(valores)}{random.choice(valores)}{random.choice(valores)}')

        self.user.post_moneyHand(ctx.guild.id, ctx.author.id, int(d))
        await ctx.send(embed=discord.Embed(color=0x444444, description=f"**{ctx.author.mention}: Reclamou seu Daily Reward no valor de: `${d}`.**"))

    @commands.check(checks.whitelist)
    @commands.cooldown(1, 900, commands.BucketType.member)
    @_bank.command(name="depositar", alises=["deposit"], no_pm=True, usage="[p]banco depositar [valor]")
    async def deposit(self, ctx, Money:int=None):
        if self.guild.get_whitelist(ctx.guild.id) == ctx.channel.id or self.guild.get_whitelist(ctx.guild.id) == 0:
            if self.check.guild(ctx.guild.id) is False:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você precisa configurar o servidor na database.", color=0xef0027))

            if self.guild.get_systemEconomy(ctx.guild.id) == 'False':
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Sistema de economia está desativado neste grupo.", color=0xef0027).set_footer(text="Para tivar use o comando: [p]set economy"))

            if Money < 0:
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Valor não aceito.", color=0xef0027))

            Hand = self.user.get_moneyHand(ctx.guild.id, ctx.author.id)

            #newMoneyPorcentage = Money - (Money * 10 / 100)

            if Hand >= Money:
                self.user.post_moneyHand(ctx.guild.id, ctx.author.id, -Money)
                self.user.post_moneyBank(ctx.guild.id, ctx.author.id, Money)
                
                embed = discord.Embed(title=f"{DepositI} Banco - {ctx.guild.name}", color=0x00ef5b, timestamp=datetime.utcnow())
                embed.add_field(name=f"{NameI}Nome:", value=f'**```{ctx.author.name}```**')
                embed.add_field(name=f"{IdI}ID:", value=f'**```{ctx.author.id}```**')
                embed.add_field(name=f"{BankI}Banco:", value=f'**```${Money}```**', inline=False)

            elif Hand < Money:
                embed = discord.Embed(title=f"{DepositI} Banco - {ctx.guild.name}", color=0xef0027, timestamp=datetime.utcnow())
                embed.add_field(name=f"{NameI}Nome:", value=f'**```{ctx.author.name}```**')
                embed.add_field(name=f"{IdI}ID:", value=f'**```{ctx.author.id}```**')
                embed.add_field(name=f"{BankI}Banco:", value="**```Abstinência do valor requisitado!```**", inline=False)

            embed.set_footer(text="Dinheiro não real!")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027), delete_after=15)
    
    @commands.check(checks.whitelist)
    @_bank.command(name="sacar", alises=["draw"], no_pm=True, usage="[p]banco sacar [valor]")
    async def draw(self, ctx, Money:int=None):
        if self.guild.whitelist(ctx.guild.id) == ctx.channel.id or self.guild.get_whitelist(ctx.guild.id) == 0:
            if self.check.guild(ctx.guild.id) is False:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você precisa configurar o servidor na database.", color=0xef0027))

            if self.guild.get_systemEconomy(ctx.guild.id) == 'False':
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Sistema de economia está desativado neste grupo.", color=0xef0027).set_footer(text="Para tivar use o comando: [p]set economy"))

            if Money < 0:
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Valor não aceito.", color=0xef0027))

            Bank = self.user.get_moneyBank(ctx.guild.id, ctx.author.id)

            if Bank >= Money:
                self.user.post_moneyHand(ctx.guild.id, ctx.author.id, Money)
                self.user.post_moneyBank(ctx.guild.id, ctx.author.id, -Money)

                embed = discord.Embed(title=f"{AtmI} Banco - {ctx.guild.name}", color=0x00ef5b, timestamp=datetime.utcnow())
                embed.add_field(name=f"{NameI}Nome:", value=f'**```{ctx.author.name}```**')
                embed.add_field(name=f"{IdI}ID:", value=f'**```{ctx.author.id}```**')
                embed.add_field(name=f"{BankI}Banco:", value=f'**```${Money}```**', inline=False)

            elif Bank < Money:
                embed = discord.Embed(title=f"{AtmI} Banco - {ctx.guild.name}", color=0xef0027, timestamp=datetime.utcnow())
                embed.add_field(name=f"{NameI}Nome:", value=f'**```{ctx.author.name}```**')
                embed.add_field(name=f"{IdI}ID:", value=f'**```{ctx.author.id}```**')
                embed.add_field(name=f"{BankI}Banco:", value="**```Abstinência do valor requisitado!```**", inline=False)

            embed.set_footer(text="Dinheiro não real!")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027), delete_after=15)
    
    @commands.check(checks.whitelist)
    @_bank.command(name="transferir", aliases=["transfer"], no_pm=True, usage="[p]banco transferir [membro] [valor]")
    async def transfer(self, ctx, Member:discord.Member=None, Money:int=None):
        if self.guild.get_whitelist(ctx.guild.id) == ctx.channel.id or self.guild.get_whitelist(ctx.guild.id) == 0:
            if self.check.guild(ctx.guild.id) is False:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você precisa configurar o servidor na database.", color=0xef0027))

            if self.guild.get_systemEconomy(ctx.guild.id) == 'False':
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Sistema de economia está desativado neste grupo.", color=0xef0027).set_footer(text="Para tivar use o comando: [p]set economy"))

            if Member is None:
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Membro não informado.", color=0xef0027))
            if Money is None:
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Valor não informado.", color=0xef0027))
            if Money < 0:
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Valor não aceito.", color=0xef0027))

            Bank = self.user.get_moneyBank(ctx.guild.id, ctx.author.id)

            if Bank >= Money:
                self.user.post_moneyBank(ctx.guild.id, Member.id, Money)
                self.user.post_moneyBank(ctx.guild.id, ctx.author.id, -Money)

                embed = discord.Embed(title=f"{TransferI} Banco - {ctx.guild.name}", color=0x00ef5b, timestamp=datetime.utcnow())
                embed.add_field(name=f"{NameI}Nome:", value=f'**```{ctx.author.name}```**')
                embed.add_field(name=f"{IdI}ID:", value=f'**```{ctx.author.id}```**')
                embed.add_field(name=f"{PersonI}Destinatário:", value=f"**```{Member.name}```**")
                embed.add_field(name=f"{BankI}Banco:", value=f'**```${Money}```**', inline=False)
                embed.set_footer(text="Transferencia aprovada!")
            elif Bank < Money:
                embed = discord.Embed(title=f"{TransferI} Banco - {ctx.guild.name}", color=0xef0027, timestamp=datetime.utcnow())
                embed.add_field(name=f"{NameI}Nome:", value=f'**```{ctx.author.name}```**')
                embed.add_field(name=f"{IdI}ID:", value=f'**```{ctx.author.id}```**')
                embed.add_field(name=f"{PersonI}Destinatário:", value=f"**```{Member.name}```**")
                embed.add_field(name=f"{BankI}Banco:", value="**```Abstinência do valor requisitado!```**", inline=False)
                embed.set_footer(text="Transferencia reprovada!")

            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027), delete_after=15)

    @commands.check(checks.whitelist)
    @_bank.command(name="extrato", aliases=["extract"], no_pm=True, usage="[p]banco extrato")
    async def extract(self, ctx):
        if self.guild.get_whitelist(ctx.guild.id) == ctx.channel.id or self.guild.get_whitelist(ctx.guild.id) == 0:
            if self.check.guild(ctx.guild.id) is False:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você precisa configurar o servidor na database.", color=0xef0027))

            if self.guild.get_systemEconomy(ctx.guild.id) == 'False':
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Sistema de economia está desativado neste grupo.", color=0xef0027).set_footer(text="Para tivar use o comando: [p]set economy"))

            Hand = self.user.get_moneyHand(ctx.guild.id, ctx.author.id)
            Bank = self.user.get_moneyBank(ctx.guild.id, ctx.author.id)

            embed = discord.Embed(title=f"{ExtractI} Banco - {ctx.guild.name}", color=0x00ef5b, timestamp=datetime.utcnow())
            embed.add_field(name=f"{NameI}Nome:", value=f'**```{ctx.author.name}```**')
            embed.add_field(name=f"{IdI}ID:", value=f'**```{ctx.author.id}```**')
            embed.add_field(name=f"{BankI}Banco:", value=f'**```${Bank}```**', inline=False)
            embed.add_field(name=f"{WalletI}Carteira:", value=f'**```${Hand}```**', inline=False)
            embed.add_field(name=f"{MoneyI}Total:", value=f'**```${int(Bank)+int(Hand)}```**', inline=False)
            embed.set_footer(text="Dinheiro não real!")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027), delete_after=15)

    @commands.check(checks.whitelist)
    @_bank.command(name="classificação", aliases=["rank","ranking"], no_pm=True, usage="[p]banco rank")
    async def ranking(self, ctx):
        if self.guild.get_whitelist(ctx.guild.id) == ctx.channel.id or self.guild.get_whitelist(ctx.guild.id) == 0:
            if self.check.guild(ctx.guild.id) is False:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você precisa configurar o servidor na database.", color=0xef0027))

            if self.guild.get_systemEconomy(ctx.guild.id) == 'False':
                return await ctx.send(embed=discord.Embed(description=f"{BankI} Sistema de economia está desativado neste grupo.", color=0xef0027).set_footer(text="Para tivar use o comando: [p]set economy"))

            await ctx.send(embed=discord.Embed(title=f"{RankI}Banco - {ctx.guild.name}", color=0x444444, description=self.user.get_moneyRank(ctx.guild.id, ctx.author.id)))
        else:
            return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027), delete_after=15)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            if self.guild.get_whitelist(ctx.guild.id) == ctx.channel.id or self.guild.get_whitelist(ctx.guild.id) == 0:
                min, sec = divmod(error.retry_after, 60)
                h, min = divmod(min, 60)
                if min == 0.0 and h == 0:
                    await ctx.send(embed=discord.Embed(color=0xef0027, description=f"**{ctx.author.mention} : Espere por ``{round(sec)}`` segundos.**"))
                else:
                    await ctx.send(embed=discord.Embed(color=0xef0027, description=f"**{ctx.author.mention} : Só poderá pegar outro Daily Reward em ``{round(h)}`` hora(s) e ``{round(min)}`` minuto(s).**"))
            else:
                await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027))
        
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027))
    
    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            min, sec = divmod(error.retry_after, 60)
            h, min = divmod(min, 60)

            if min == 0.0 and h == 0:
                await ctx.send(embed=discord.Embed(color=0xef0027, description=f"**{ctx.author.mention} : Espere por ``{round(sec)}`` segundos.**"))
            else:
                await ctx.send(embed=discord.Embed(color=0xef0027, description=f"**{ctx.author.mention} : Só podera depositar em ``{round(h)}`` hora(s) e ``{round(min)}`` minuto(s).**"))
        
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027))

    @draw.error
    async def draw_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027))

    @transfer.error
    async def transfer_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027))

    @extract.error
    async def extract_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027))

    @ranking.error
    async def ranking_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, você não pode executar comandos nesse chat.", color=0xef0027))

def setup(client):
    client.add_cog(MyBank(client))