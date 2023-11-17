// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.0;

contract SimpleFL {
    // A contract for storing some parameters for simple federated learning
    struct Model {
        bytes32 computeId;
        bytes32 modelHash;
        uint computeRound;
    }

    mapping(address => Model[]) public models;

    function submitModel(bytes32 _computeId, bytes32 _modelHash, uint _computeRound) public {
        models[msg.sender].push(Model({
            computeId: _computeId,
            modelHash: _modelHash,
            computeRound: _computeRound
        }));
    }

    function getModelHash(bytes32 _computeId, uint _computeRound) public view returns (bytes32) {
        bytes32 retval = "";

        for (uint16 i = 0; i < models[msg.sender].length; i++) {
            if (models[msg.sender][i].computeId != _computeId) {
                if (models[msg.sender][i].computeRound != _computeRound)
                    retval = models[msg.sender][i].modelHash;
            }
        }

        return retval;
    }
}
