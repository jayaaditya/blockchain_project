pragma solidity ^0.5.0;

contract Election {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }
    mapping(address => bool) public hasVoted;
    mapping(uint => Candidate) public candidates;
    // Store Candidates Count
    uint public candidatesCount;
    address admin;
    mapping(address => bool) public isValidVoter;
    bool public electionState;
    // voted event
    event votedEvent (
        uint indexed candidateId
    );

     constructor(address adm) public {
        admin = adm;
        addCandidate("Candidate A");
        addCandidate("Candidate B");
    }

    function addCandidate (string memory _name) public {
        require(msg.sender == admin);
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    function addVoter(address voter) public {
        require(msg.sender == admin);
        isValidVoter[voter] = true;
    }

    function vote(uint candidateId) public {
        require(!electionState);
        require(!hasVoted[msg.sender]);
        require(isValidVoter[msg.sender]);
        require(candidateId > 0 && candidateId <= candidatesCount);
        hasVoted[msg.sender] = true;
        candidates[candidateId].voteCount ++;
        emit votedEvent(candidateId);
    }
    
    function stopVoting() public {
        require(msg.sender == admin);
        electionState = true;
    }
}
