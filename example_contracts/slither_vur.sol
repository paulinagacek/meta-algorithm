//SPDX-License-Identifier:MIT
pragma solidity ^0.8.9;

/**
 * @dev Interface of the ERC20 standard as defined in the EIP.
 */
interface IERC20 {
    /**
     * @dev Emitted when `value` tokens are moved from one account (`from`) to
     * another (`to`).
     *
     * Note that `value` may be zero.
     */
    event Transfer(address indexed from, address indexed to, uint256 value);

    /**
     * @dev Emitted when the allowance of a `spender` for an `owner` is set by
     * a call to {approve}. `value` is the new allowance.
     */
    event Approval(address indexed owner, address indexed spender, uint256 value);

    /**
     * @dev Returns the amount of tokens in existence.
     */
    function totalSupply() external view returns (uint256);

    /**
     * @dev Returns the amount of tokens owned by `account`.
     */
    function balanceOf(address account) external view returns (uint256);

    /**
     * @dev Moves `amount` tokens from the caller's account to `to`.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits a {Transfer} event.
     */
    function transfer(address to, uint256 amount) external returns (bool);

    /**
     * @dev Returns the remaining number of tokens that `spender` will be
     * allowed to spend on behalf of `owner` through {transferFrom}. This is
     * zero by default.
     *
     * This value changes when {approve} or {transferFrom} are called.
     */
    function allowance(address owner, address spender) external view returns (uint256);

    /**
     * @dev Sets `amount` as the allowance of `spender` over the caller's tokens.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * IMPORTANT: Beware that changing an allowance with this method brings the risk
     * that someone may use both the old and the new allowance by unfortunate
     * transaction ordering. One possible solution to mitigate this race
     * condition is to first reduce the spender's allowance to 0 and set the
     * desired value afterwards:
     * https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
     *
     * Emits an {Approval} event.
     */
    function approve(address spender, uint256 amount) external returns (bool);

    /**
     * @dev Moves `amount` tokens from `from` to `to` using the
     * allowance mechanism. `amount` is then deducted from the caller's
     * allowance.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits a {Transfer} event.
     */
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

contract Vulnerability {
    address private USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    mapping(address => uint256) public balances;
    uint256 public lotteryWinningNumber;
    address public owner;

    constructor(){
        owner = msg.sender;
    }

    //Using strict equality is a vulnerability
    function fund_reached() public view returns (bool) {
        return address(this).balance == 100 ether;
    }

    //from field is dangerous to use in this case because if Person A has given allowance to this contract for some amount of tokens,
    //Person B can easily transfer those tokens to his own account
    function USDCTransfer(
        address _from,
        address _to,
        uint256 _amount
    ) public {
        IERC20(USDC).transferFrom(_from, _to, _amount);
    }

    //anyone can kill the contract and claim any funds to their own address
    function kill() public {
        selfdestruct(payable(msg.sender));
    }

    //Using delegate should only be done on trusted contracts. so _to address should not be given here
    function delegate(address _to, bytes memory _data) public {
        (bool result, ) = _to.delegatecall(_data);
    }

    //Reentrancy attack. Balances variable is being updated after transfer here.
    function withdraw(uint256 _amount) public {
        if (balances[msg.sender] >= _amount) {
            (bool result, ) = msg.sender.call{value: _amount}("");
            require(result, "Could not transfer");
            balances[msg.sender] -= _amount;
        }
    }

    //Using of Block.timestamp, blockhash and now in random number generation is highly discouraged
    //Use of Chainlink VRF is preferred.
    function winLottery() external{
      lotteryWinningNumber = uint256(block.timestamp) % 10;
    }

    uint256 amt;
    //Dividing first can cause serious problems if b is greater than a.
    //So always multiply first and then divide
    function divideBeforeMultiply(uint256 a, uint256 b, uint256 c) public{
        amt = (a / b) * c;
    }

    //Avoid usage of Tx.origin 
    function txOriginExploit(uint256 _amount) public{
        require(tx.origin == owner);
        withdraw(_amount);
    }

    //Since to is not initialized. It will be 0x0 address. and all money will be lost
    function transferMoney() payable public{
        address to;
        (bool result, ) = to.call{value: address(this).balance}("");
        require(result, "Could not transfer");
    }


//The below shows the incorrect usage of storage and memory variables
    uint[1] public x; // storage

    function f() public {
        f1(x); // update x
        f2(x); // do not update x
    }

    function f1(uint[1] storage arr) internal { // by reference
        arr[0] = 1;
    }

    function f2(uint[1] memory arr) internal pure{ // by value
        arr[0] = 2;
    }
}