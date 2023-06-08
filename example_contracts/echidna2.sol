contract Test {
  event Flag(bool);

  bool private flag0 = true;
  bool private flag1 = true;
  bool private flag2 = true;

  function set0(int val) public returns (bool){
    if (val % 100 == 0) 
      flag0 = false;
  }

  function set1(int val) public returns (bool){
    if (val % 10 == 0 && !flag0) 
      flag1 = false;
  }

  function set2(int val) public returns (bool){
    if (val != 10) 
      flag2 = false;
  }

  function echidna_alwaystrue() public returns (bool){
    return(true);
  }

  function echidna_alwaystrue2() public returns (bool){
    return(true);
  }

  function echidna_alwaystrue3() public returns (bool){
    return(true);
  }

  function echidna_revert_always() public returns (bool){
    revert();
  }

  function echidna_revert_always2() public returns (bool){
    revert();
  }

  function echidna_revert_always3() public returns (bool){
    revert();
  }

  function echidna_revert_always4() public returns (bool){
    revert();
  }

  function echidna_revert_always5() public returns (bool){
    revert();
  }

  function echidna_revert_always6() public returns (bool){
    revert();
  }

  function echidna_sometimesfalse() public returns (bool){
    emit Flag(flag0);
    emit Flag(flag1);
    return(flag1);
  }

  function echidna_sometimesfalse2() public returns (bool){
    emit Flag(flag2);
    return(flag2);
  }

  function echidna_sometimesfalse3() public returns (bool){
    emit Flag(flag2);
    return(flag2);
  }
}