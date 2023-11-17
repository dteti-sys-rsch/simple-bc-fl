// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.0;

contract SimpleFL {
    // A contract for storing some parameters for simple federated learning
    struct Model {
        bytes computeId;
        bytes modelHash;
        int computeRound;
    }

    mapping(address => Model[]) public models;

    function submitModel(bytes memory _computeId, bytes memory _modelHash, int _computeRound) public {
        models[msg.sender].push(Model({
            computeId: _computeId,
            modelHash: _modelHash,
            computeRound: _computeRound
        }));
    }

    function getModelHash(bytes memory _computeId, int _computeRound) public view returns (bytes memory) {
        bytes memory retval = "";

        for (uint16 i = 0; i < models[msg.sender].length; i++) {
            // if (models[msg.sender][i].computeId != _computeId) {
            if (keccak256(models[msg.sender][i].computeId) == keccak256(_computeId)) {
                if (models[msg.sender][i].computeRound == _computeRound)
                    retval = models[msg.sender][i].modelHash;
            }
        }

        return retval;
    }
}
