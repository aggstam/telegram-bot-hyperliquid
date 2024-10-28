# --------------------------------------------------------------------------
#
# Very basic telegram bot to retrieve information using Hyperliquid(https://hyperliquid.xyz/) API.
#
# Author: Aggelos Stamatiou, October 2024
#
# This source code is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this source code. If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------

import sys
from hyperliquid.info import Info
from hyperliquid.utils import constants
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Execute an info request toward HL for provided address and return the retrieved info.
# Retrieved information is formatted into a human readable message.
def hl_vault_info(address: str) -> str:
    # Define and execute the request
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    data = info.user_state(address)

    # Format retrieved data
    account_value = 0
    if data['marginSummary']['accountValue'] is not None:
        account_value = float(data['marginSummary']['accountValue'])
    total_margin_used = 0
    if data['marginSummary']['totalMarginUsed'] is not None:
        total_margin_used = float(data['marginSummary']['totalMarginUsed'])
    total_positions = len(data['assetPositions'])

    message = f'🚀 Trading Account Update 🚀\n\n'
    message += f'💰 Account Value: ${account_value:,.2f}\n'
    message += f'💼 Total Margin Used: ${total_margin_used:,.2f}\n'
    if account_value > 0:
        message += f'Margin Usage: {total_margin_used/account_value:.2%}\n'
    else:
        message += f'Margin Usage: 0\n'
    message += f'Total positions: {total_positions}\n\n'

    # Parse vault positions
    for position in data['assetPositions']:
        position = position['position']
        message += '📊 Position Details:\n'
        message += f'Coin: {position['coin']}\n'
        message += f'Size: {float(position['szi']):,.0f} coins\n'
        message += f'Entry Price: ${float(position['entryPx']):,.6f}\n'
        message += f'Position Value: ${float(position['positionValue']):,.2f}\n'

        unrealized_pnl = 0
        if position['unrealizedPnl'] is not None:
            unrealized_pnl = float(position['unrealizedPnl'])
        message += f'Unrealized P&L: ${unrealized_pnl:,.2f}'
        if unrealized_pnl > 0:
            message += ' 📈\n'
        else:
            message += ' 📉\n'

        message += f'Liquidation Price: ${float(position['liquidationPx']):,.6f}\n'
        message += f'Max Leverage: {position['maxLeverage']}x\n\n'

        cumulative_funding = position['cumFunding']
        message += '💸 Cumulative Funding:\n'
        message += f'All Time: ${float(cumulative_funding['allTime']):,.2f}\n'
        message += f'Since Open: ${float(cumulative_funding['sinceOpen']):,.2f}\n\n'

    return message

# Parse prompt into an HL command and its parts, then execute it and return its output.
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Set response
    response = 'Unknown Hyperliquid command provided'

    # Handle command (first arg)
    try:
        # Vault info command
        if context.args[0] == 'vault':
            # Use default address if none was provided
            if len(context.args) == 1:
                response = hl_vault_info(context.application.hl_default_vault)
            else:
                response = hl_vault_info(context.args[1])

        # We can add rest commands handling here
    except Exception as error:
        response = f'Hyperliquid error: {error}'

    await update.message.reply_text(response)

# Main function
def main():
    # Initialize bot
    bot_token = sys.argv[1]
    hl_default_vault = sys.argv[2]
    bot = Application.builder().token(bot_token).build()
    bot.hl_default_vault = hl_default_vault

    # Add the bot command handler
    bot.add_handler(CommandHandler('hl', handle_command, has_args=True))

    # Run the bot until the user presses Ctrl-C
    bot.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
